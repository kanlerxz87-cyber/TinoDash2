#!/usr/bin/env node
/*
 * Headless smoke test for calculator.js — the browser-only seven-path model.
 *
 * No DOM library and no network: a ~40-line stub of the handful of DOM calls the
 * calculator uses is enough to prove that (a) the default page state is honest,
 * (b) submitting a filled form produces seven ranked rows, and (c) the module
 * never reaches for fetch / XHR / storage / cookies.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "calculator.js"), "utf8");

const failures = [];
function check(ok, message) {
  if (!ok) failures.push(message);
}

/* ---------- 1. the module must not be able to send or persist anything ---------- */
const banned = [
  [/\bfetch\s*\(/, "fetch("],
  [/XMLHttpRequest/, "XMLHttpRequest"],
  [/sendBeacon/, "sendBeacon"],
  [/localStorage/, "localStorage"],
  [/sessionStorage/, "sessionStorage"],
  [/document\.cookie/, "document.cookie"],
  [/indexedDB/, "indexedDB"],
  [/importScripts/, "importScripts"],
];
for (const [pattern, label] of banned) {
  check(!pattern.test(source), "calculator.js must stay browser-only but references " + label);
}
// A remote URL in a string literal would be a network path we did not intend.
check(
  !/src\s*=\s*["']https?:/.test(source) && !/["']https?:\/\/[a-z]/i.test(source),
  "calculator.js must not contain remote URLs"
);

/* ---------- 2. drive the real file against a minimal DOM ---------- */
function makeEl(id) {
  return {
    id: id,
    value: "",
    textContent: "",
    innerHTML: "",
    hidden: false,
    style: {},
    children: [],
    listeners: {},
    appendChild(child) {
      this.children.push(child);
    },
    addEventListener(event, fn) {
      this.listeners[event] = fn;
    },
  };
}

const elements = {};
function byId(id) {
  if (!elements[id]) elements[id] = makeEl(id);
  return elements[id];
}

let readyHandler = null;
global.document = {
  getElementById: byId,
  createElement: () => makeEl("created"),
  addEventListener: (event, fn) => {
    if (event === "DOMContentLoaded") readyHandler = fn;
  },
};

let run = null;
const form = byId("calcForm");
form.addEventListener = function (event, fn) {
  if (event === "submit") run = fn;
  this.listeners[event] = fn;
};
byId("calcStatus");
// mirror the markup: <div id="calcOut" hidden>
byId("calcOut").hidden = true;

eval(source);

/* ---------- 3. blank page state ---------- */
check(typeof readyHandler === "function", "calculator.js did not register a DOMContentLoaded handler");
if (typeof readyHandler === "function") readyHandler();
check(/blank/i.test(elements.calcStatus.textContent), "blank form should say the inputs are blank on purpose");
check(elements.calcOut.hidden === true || elements.calcOut.hidden === undefined,
  "results must stay hidden until the form is submitted");

/* ---------- 4. filled submission ---------- */
const inputs = {
  horizon: "10", value: "1000000", basis: "1000000", saleCostPct: "6",
  appLow: "2", appHigh: "4", rentLow: "4000", rentHigh: "6000", imputedRent: "5000",
  propTax: "12000", insurance: "2000", utilities: "1000", maint: "0.6", capitalReserve: "0.5",
  vacancyPct: "5", inflPct: "3", retLow: "4", retHigh: "8", taxDragPct: "0.5",
  treasuryPct: "4", parkMonths: "24", phaseMonths: "36", otherCaIncome: "0",
  gainTaxPct: "33", reserve: "50000",
};
for (const [id, value] of Object.entries(inputs)) byId(id).value = value;

check(typeof run === "function", "calculator.js did not bind a submit handler");
if (typeof run === "function") {
  let threw = null;
  try {
    run({ preventDefault() {} });
  } catch (err) {
    threw = err;
  }
  check(threw === null, "submitting the form threw: " + (threw && threw.message));
  check(elements.calcRows.children.length === 7,
    "expected 7 path rows, got " + elements.calcRows.children.length);
  const ranked = elements.calcRank.innerHTML || "";
  check(/Base-case ranking/.test(ranked), "ranking block was not written");
  check((ranked.match(/\$\d/g) || []).length >= 7, "ranking should report a dollar outcome for each path");
  check(elements.calcOut.hidden === false, "results must be revealed after a valid submission");
  check(/browser/i.test(elements.calcStatus.textContent), "status should confirm the computation stayed in the browser");
}

/* ---------- 5. rounding rule: outputs are rounded to the nearest $10 ---------- */
const rounded = (source.match(/Math\.round\([^)]*\/\s*10\s*\)\s*\*\s*10/g) || []).length;
check(rounded > 0, "calculator.js should round displayed money to the nearest $10");

if (failures.length) {
  console.error("Calculator smoke test FAILED:");
  for (const failure of failures) console.error(" - " + failure);
  process.exit(1);
}
console.log("Calculator smoke test passed: " + elements.calcRows.children.length +
  " ranked paths from a filled form, blank state honest, no network or storage APIs referenced.");

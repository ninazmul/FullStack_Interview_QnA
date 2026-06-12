from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pdfencrypt import StandardEncryption

W, H = A4

NAVY    = colors.HexColor('#0C447C')
BLUE    = colors.HexColor('#185FA5')
LBLUE   = colors.HexColor('#E6F1FB')
GREEN   = colors.HexColor('#3B6D11')
LGREEN  = colors.HexColor('#EAF3DE')
PURPLE  = colors.HexColor('#3C3489')
LPURPLE = colors.HexColor('#EEEDFE')
AMBER   = colors.HexColor('#854F0B')
LAMBER  = colors.HexColor('#FAEEDA')
CORAL   = colors.HexColor('#993C1D')
LCORAL  = colors.HexColor('#FAECE7')
PINK    = colors.HexColor('#72243E')
LPINK   = colors.HexColor('#FBEAF0')
TEAL    = colors.HexColor('#0D7A80')
LTEAL   = colors.HexColor('#E0F4F5')
OLIVE   = colors.HexColor('#4D5B2A')
LOLIVE  = colors.HexColor('#F0F4E4')
GRAY    = colors.HexColor('#444441')
LGRAY   = colors.HexColor('#F1EFE8')
DGRAY   = colors.HexColor('#2C2C2A')
CODE_BG = colors.HexColor('#F1EFE8')
CODE_FG = colors.HexColor('#26215C')
WHITE   = colors.white
BORDER  = colors.HexColor('#B5D4F4')
GOLD    = colors.HexColor('#D4A017')
GOLD_DIM = colors.HexColor('#D6D0C0')

PHASE_COLORS = [
    (BLUE,   LBLUE),
    (GREEN,  LGREEN),
    (PURPLE, LPURPLE),
    (AMBER,  LAMBER),
    (CORAL,  LCORAL),
    (PINK,   LPINK),
    (TEAL,   LTEAL),
    (OLIVE,  LOLIVE),
]

# --------------------------------------------------------------------------
# Data: (LEVEL, RATING 1-5, QUESTION, ANSWER, CODE, TIP)
#   RATING = interview frequency:  5=almost always  4=very often  3=common  2=sometimes  1=rare
# --------------------------------------------------------------------------

QNA = {
    # =====================================================================
    "Phase 1: JavaScript & TypeScript Fundamentals": [
        ("BASIC", 5, "What is the difference between var, let, and const?",
         "var is function-scoped and hoisted (initialized to undefined). let and const are block-scoped and live in the Temporal Dead Zone until declared. const cannot be reassigned, but its object/array contents can still be mutated.",
         "var x = 1;\nif (true) {\n  var x = 10;  // same variable — function-scoped\n  let y = 20;  // block-scoped, dies here\n}\nconsole.log(x); // 10\n// console.log(y); // ReferenceError",
         "Prefer const by default; use let when reassignment is needed; avoid var in modern code."),

        ("BASIC", 5, "What is hoisting in JavaScript?",
         "Hoisting moves variable and function declarations to the top of their scope before execution. var is hoisted and initialized to undefined. Function declarations are fully hoisted. let and const are hoisted but stay in the Temporal Dead Zone (TDZ) — accessing them before declaration throws a ReferenceError.",
         "console.log(a); // undefined (var hoisted)\nvar a = 5;\n\ngreet(); // works — function fully hoisted\nfunction greet() { return 'hello'; }\n\nconsole.log(b); // ReferenceError (TDZ)\nlet b = 10;",
         "The TDZ is the gap between entering scope and the actual declaration line."),

        ("BASIC", 5, "Explain JavaScript closures with an example.",
         "A closure is a function that remembers the variables from its birthplace (outer scope) even after that outer function has returned. Think of it as a backpack — the inner function carries its outer variables with it wherever it goes. Closures enable data encapsulation, factory functions, and stateful logic.",
         "function makeCounter() {\n  let count = 0;\n  return {\n    increment: () => ++count,\n    decrement: () => --count,\n    value: () => count,\n  };\n}\nconst c = makeCounter();\nc.increment(); c.increment();\nconsole.log(c.value()); // 2",
         "Each call to makeCounter() creates an independent closure with its own count."),

        ("BASIC", 5, "What is the difference between == and ===?",
         "== (loose equality) coerces types before comparing — it tries to make both sides the same type. === (strict equality) compares value AND type with no coercion. Always use === in production code to avoid subtle type-coercion bugs.",
         "0 == false      // true  (coercion)\n0 === false     // false (different types)\nnull == undefined  // true\nnull === undefined // false\n'' == 0         // true\n'' === 0        // false",
         "Use === everywhere. The only valid use of == is null-check: x == null catches both null and undefined."),

        ("BASIC", 5, "What are JavaScript primitive types?",
         "Remember: SNBBUNS — String, Number, BigInt, Boolean, Undefined, Null, Symbol. These 7 are primitives — immutable and compared by value. Everything else (arrays, objects, functions, maps) is a reference type — compared by reference.",
         "typeof 'hi'        // 'string'\ntypeof 42          // 'number'\ntypeof true        // 'boolean'\ntypeof undefined   // 'undefined'\ntypeof null        // 'object' (JS bug)\ntypeof []          // 'object'\ntypeof function(){} // 'function'",
         "typeof null === 'object' is a historical JavaScript bug — use null === x to check for null."),

        ("BASIC", 5, "What is the difference between null and undefined?",
         "undefined = 'nobody assigned a value yet' — it's the default empty state. null = 'I intentionally set this to nothing' — it's a deliberate absence. typeof undefined is 'undefined'; typeof null is 'object' (historical bug).",
         "let a;             // undefined automatically\nlet b = null;      // intentional empty\n\nfunction getUser(id) {\n  if (!id) return null; // intentional: no user\n}\n\nconsole.log(a == b);  // true (loose)\nconsole.log(a === b); // false (strict)",
         "Use null when you intentionally want to represent 'no value'. Let undefined arise naturally."),

        ("BASIC", 5, "Explain event delegation and event bubbling.",
         "Event bubbling: when an event fires on an element, it bubbles UP through all its parents (child → parent → grandparent → document). Event delegation: instead of attaching listeners to every child, attach ONE listener to the parent and use event.target to identify which child was clicked. This is more memory-efficient and works for dynamically added elements.",
         "// Instead of 1000 listeners on 1000 items:\nul.addEventListener('click', e => {\n  if (e.target.tagName === 'LI') {\n    console.log('Clicked:', e.target.textContent);\n  }\n});\n\n// Phases: capture (down) → target → bubble (up)\n// stopPropagation() stops the chain\n// preventDefault() cancels default action",
         "Event delegation is how React handles events internally — one listener at the root."),

        ("BASIC", 5, "What does the 'this' keyword refer to in different contexts?",
         "this depends on HOW a function is called, not WHERE it's defined. Global: window/undefined. Object method: the object. Constructor (new): the new instance. Arrow function: inherits this from enclosing scope (lexical). call/apply/bind: whatever you pass. This is the #1 gotcha in JavaScript.",
         "const obj = {\n  name: 'Nazmul',\n  greet() { return this.name; },      // 'Nazmul'\n  arrow: () => this.name,              // undefined (lexical)\n};\n\nfunction show() { console.log(this); }\nshow();           // window (or undefined in strict)\nnew show();       // new object\nshow.call(obj);   // obj",
         "Arrow functions don't have their own this — they capture it from where they're defined."),

        ("BASIC", 4, "Explain destructuring, spread, and rest operators.",
         "Destructuring extracts values from arrays/objects into variables. Spread (...) expands an iterable into individual elements. Rest (...) collects remaining elements into an array/object. Same syntax (...) but opposite directions — spread unpacks, rest packs.",
         "// Destructuring\nconst { name, age = 25 } = user;\nconst [first, ...rest] = [1, 2, 3]; // rest = [2,3]\n\n// Spread — clone + merge\nconst copy = { ...obj, newProp: 'val' };\nconst merged = [...arr1, ...arr2];\n\n// Rest parameters\nfunction sum(...nums) {\n  return nums.reduce((a, b) => a + b, 0);\n}",
         "Spread = unpack (array/object → elements). Rest = pack (elements → array/object)."),

        ("BASIC", 4, "What are optional chaining (?.) and nullish coalescing (??) operators?",
         "Optional chaining (?.) short-circuits to undefined if any part is null/undefined — no more 'cannot read property of undefined' errors. Nullish coalescing (??) returns the right side only when the left is null or undefined (not for 0, '', or false like || does).",
         "// Optional chaining\nconst city = user?.address?.city; // safe\nconst first = arr?.[0];\nconst result = obj?.method?.();\n\n// Nullish coalescing\nconst port = config.port ?? 3000;\n// port = 0 → 0 (keeps falsy values!)\n// port = null → 3000\n\n// Compare with ||\nconst port2 = config.port || 3000;\n// port = 0 → 3000 (BUG — treats 0 as falsy!)",
         "Use ?? when 0, '', and false are valid values. Use || only for truly falsy defaults."),

        ("BASIC", 4, "What is the difference between Map and Object?",
         "Map allows any type as key (objects, functions, numbers); Object keys are always strings/symbols. Map maintains insertion order and has a .size property. Map is faster for frequent add/delete operations. Use Map for dynamic key-value lookups; Object for structured records.",
         "const map = new Map();\nmap.set({id: 1}, 'user1'); // object as key!\nmap.set(42, 'answer');\nmap.size; // 2\n\n// Iteration\nfor (const [key, val] of map) { ... }\n\n// Object — keys coerced to strings\nconst obj = {};\nobj[1] = 'one';\nobj['1'] = 'ONE'; // overwrites! same key\nObject.keys(obj); // ['1']",
         "Map for dictionaries with dynamic keys. Object for shaped data with known properties."),

        ("INTERMEDIATE", 5, "Explain the JavaScript event loop.",
         "JavaScript is single-threaded but non-blocking. The event loop is the traffic controller — it processes one task, then checks the microtask queue (Promises, queueMicrotask), drains it completely, then picks the next macrotask (setTimeout, setInterval). Microtasks always run before macrotasks.",
         "console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');\n// Output: 1, 4, 3, 2\n// Sync first → microtask (3) → macrotask (2)",
         "setTimeout(fn, 0) does not mean immediate — it means 'run after current + microtasks finish'."),

        ("INTERMEDIATE", 5, "What is the difference between Promise, async/await, and callbacks?",
         "Three generations of async: Callbacks (oldest, nesting hell) → Promises (.then/.catch chaining) → async/await (syntactic sugar, reads like sync code). async/await IS Promises underneath — just cleaner syntax. Always wrap await in try/catch for error handling.",
         "// Callback hell\nfetchUser(id, (err, user) => {\n  fetchPosts(user.id, (err, posts) => {\n    fetchComments(posts[0].id, (err, comments) => {});\n  });\n});\n\n// async/await (clean)\nasync function load(id) {\n  try {\n    const user = await fetchUser(id);\n    const posts = await fetchPosts(user.id);\n    const comments = await fetchComments(posts[0].id);\n  } catch(e) { console.error(e); }\n}",
         "Always handle rejections. Unhandled promise rejections crash Node.js processes."),

        ("INTERMEDIATE", 5, "Explain prototypal inheritance in JavaScript.",
         "Every JS object has a hidden [[Prototype]] link to another object. When you access a property that doesn't exist on the object, JS walks up the prototype chain until it finds it or reaches null. ES6 classes are just syntactic sugar over this prototype chain mechanism.",
         "function Animal(name) { this.name = name; }\nAnimal.prototype.speak = function() {\n  return this.name + ' speaks';\n};\n\nconst dog = new Animal('Rex');\nconsole.log(dog.speak()); // Rex speaks\nconsole.log(dog.__proto__ === Animal.prototype); // true\nconsole.log(dog.hasOwnProperty('speak')); // false",
         "hasOwnProperty distinguishes own properties from inherited prototype properties."),

        ("INTERMEDIATE", 5, "Explain debounce vs throttle.",
         "Debounce: wait until the user STOPS doing something, then fire once. Like a search box — wait until they stop typing. Throttle: fire at most once per interval, no matter how many times triggered. Like scroll events — fire every 200ms max. Both prevent performance death from rapid events.",
         "// Debounce — waits for silence\nfunction debounce(fn, ms) {\n  let timer;\n  return (...args) => {\n    clearTimeout(timer);\n    timer = setTimeout(() => fn(...args), ms);\n  };\n}\n\n// Throttle — fires at intervals\nfunction throttle(fn, ms) {\n  let last = 0;\n  return (...args) => {\n    const now = Date.now();\n    if (now - last >= ms) {\n      last = now;\n      fn(...args);\n    }\n  };\n}",
         "Debounce for search inputs. Throttle for scroll/resize. Both are critical for performance."),

        ("INTERMEDIATE", 4, "Explain the classic var + closure loop problem.",
         "With var in a for loop, all callbacks share the same variable reference because var is function-scoped. By the time callbacks execute, i holds its final value. Fix: use let (block-scoped per iteration) or an IIFE to capture each value.",
         "// Problem — prints 3,3,3\nfor (var i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 0);\n}\n\n// Fix 1: let (block-scoped)\nfor (let i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 0); // 0,1,2\n}\n\n// Fix 2: IIFE\nfor (var i = 0; i < 3; i++) {\n  ((j) => setTimeout(() => console.log(j), 0))(i);\n}",
         "This is one of the most common closure interview questions — know both fixes."),

        ("INTERMEDIATE", 4, "What is the difference between call, apply, and bind?",
         "All three let you choose what 'this' is. call() and apply() invoke the function immediately — call takes args as a list, apply takes an array (A for Array). bind() returns a NEW function with 'this' permanently locked — it doesn't invoke immediately.",
         "function greet(greeting, punct) {\n  return greeting + ', ' + this.name + punct;\n}\nconst user = { name: 'Nazmul' };\n\ngreet.call(user, 'Hello', '!');   // 'Hello, Nazmul!'\ngreet.apply(user, ['Hi', '?']);   // 'Hi, Nazmul?'\nconst fn = greet.bind(user, 'Hey');\nfn('.');  // 'Hey, Nazmul.'",
         "bind is commonly used to preserve this in class methods passed as React event handlers."),

        ("INTERMEDIATE", 4, "What are Promise.all, Promise.race, Promise.allSettled, and Promise.any?",
         "Promise.all: ALL must succeed — one failure rejects everything. Promise.race: first to settle (success or fail) wins. Promise.allSettled: waits for ALL and never rejects — gives you status of each. Promise.any: first SUCCESS wins — only rejects if ALL fail (AggregateError).",
         "const p1 = fetch('/api/users');\nconst p2 = fetch('/api/posts');\n\n// All must succeed\nconst [users, posts] = await Promise.all([p1, p2]);\n\n// Results regardless of failure\nconst results = await Promise.allSettled([p1, p2]);\nresults.forEach(r => {\n  if (r.status === 'fulfilled') console.log(r.value);\n  else console.log(r.reason);\n});",
         "Use Promise.allSettled when you need results from all — even failed — promises."),

        ("INTERMEDIATE", 4, "What are arrow functions and how do they differ from regular functions?",
         "Arrow functions have 5 key differences: 1) No own 'this' (inherits from enclosing scope), 2) No 'arguments' object, 3) Cannot be used as constructors (no new), 4) No prototype property, 5) Concise syntax. They're perfect for callbacks but wrong for object methods.",
         "// Regular function — has own 'this'\nfunction Timer() {\n  this.count = 0;\n  setInterval(function() {\n    this.count++; // 'this' is undefined in strict\n  }, 1000);\n}\n\n// Arrow function — inherits 'this'\nfunction Timer() {\n  this.count = 0;\n  setInterval(() => {\n    this.count++; // 'this' is Timer instance\n  }, 1000);\n}",
         "Never use arrow functions as object methods if you need this to refer to the object."),

        ("INTERMEDIATE", 4, "Explain JavaScript modules: ESM vs CommonJS.",
         "CommonJS (require/module.exports): synchronous, runs at runtime, used in Node.js. ESM (import/export): asynchronous, statically analyzed at compile time, supports tree-shaking. ESM is the future — Node.js 14+ supports it, browsers support it natively.",
         "// CommonJS (Node.js traditional)\nconst fs = require('fs');\nmodule.exports = { myFunc };\n\n// ESM (modern standard)\nimport fs from 'fs';\nexport const myFunc = () => {};\nexport default class MyClass {}\n\n// Key differences:\n// ESM: static imports → tree-shakeable\n// CJS: dynamic require() → can be conditional\n// ESM: top-level await supported\n// CJS: require is synchronous",
         "Use ESM for new projects. Set 'type': 'module' in package.json to enable ESM in Node.js."),

        ("INTERMEDIATE", 4, "What is the difference between Map/Set and WeakMap/WeakSet?",
         "Map/Set hold strong references — keys stay in memory forever. WeakMap/WeakSet hold weak references — keys can be garbage collected when no other references exist. WeakMap/WeakSet are not iterable and have no .size. Use them when you need to attach metadata to objects without preventing GC.",
         "const cache = new WeakMap();\n\nfunction process(obj) {\n  if (cache.has(obj)) return cache.get(obj);\n  const result = heavyComputation(obj);\n  cache.set(obj, result); // auto-removed when obj is GC'd\n  return result;\n}\n\n// Regular Map would prevent GC of obj\n// WeakMap allows GC — no memory leak\n\n// Set vs WeakSet\nconst visited = new WeakSet();\nvisited.add(node); // auto-cleaned when node is GC'd",
         "WeakMap is the correct tool for associating data with DOM nodes without memory leaks."),

        ("INTERMEDIATE", 3, "What is the difference between shallow copy and deep copy?",
         "Shallow copy duplicates the top level but nested objects share references — changing nested data in the copy changes the original. Deep copy recursively clones everything — fully independent. Spread and Object.assign are shallow. structuredClone() is the modern deep copy.",
         "const orig = { a: 1, b: { c: 2 } };\n\n// Shallow — b is shared\nconst shallow = { ...orig };\nshallow.b.c = 99;\nconsole.log(orig.b.c); // 99 (mutated!)\n\n// Deep — fully independent\nconst deep = structuredClone(orig);\ndeep.b.c = 99;\nconsole.log(orig.b.c); // 2 (safe)",
         "JSON.parse(JSON.stringify()) fails on Date, undefined, functions, and circular refs — use structuredClone."),

        ("ADVANCED", 4, "Explain TypeScript generics.",
         "Generics let you write functions/classes that work with ANY type while keeping type safety. Think of <T> as a type variable — it captures the type at call time and carries it through. Without generics you'd use 'any' and lose all type information.",
         "function identity<T>(arg: T): T { return arg; }\n\n// Real-world: typed API response\nasync function fetchData<T>(url: string): Promise<T> {\n  const res = await fetch(url);\n  return res.json() as T;\n}\n\ninterface User { id: number; name: string; }\nconst user = await fetchData<User>('/api/user/1');\nuser.name; // TypeScript knows this is string",
         "Use constraints (T extends object) to limit which types can be passed."),

        ("ADVANCED", 4, "What are TypeScript utility types?",
         "Built-in type transformers. Partial<T> makes all properties optional. Required<T> makes all mandatory. Pick<T,K> selects specific keys. Omit<T,K> removes keys. Record<K,V> maps keys to values. Readonly<T> prevents mutation. These compose like building blocks.",
         "interface User {\n  id: number; name: string;\n  email: string; age: number;\n}\n\ntype UpdateUser = Partial<User>;\n// All fields optional — for PATCH requests\n\ntype UserPreview = Pick<User, 'id' | 'name'>;\n// Only id and name\n\ntype PublicUser = Omit<User, 'email'>;\n// Everything except email\n\ntype UserMap = Record<string, User>;\n// { [key: string]: User }",
         "Combine utility types: Partial<Pick<User, 'name' | 'email'>> for partial update DTOs."),

        ("ADVANCED", 4, "What is the difference between interface and type in TypeScript?",
         "Both define shapes, but: Interfaces support 'extends' and declaration merging (same name merges automatically). Types handle unions, intersections, tuples, and mapped types. Rule of thumb: interface for object shapes, type for everything else.",
         "interface Animal { name: string; }\ninterface Dog extends Animal { breed: string; }\n\n// Declaration merging (interfaces only)\ninterface Window { myProp: string; }\ninterface Window { another: number; } // merged\n\n// Types handle unions\ntype ID = string | number;\ntype Result<T> = { data: T } | { error: string };\ntype Point = [number, number]; // tuple",
         "In a codebase, pick one and be consistent. Most teams use interface for objects, type for the rest."),

        ("ADVANCED", 4, "What is TypeScript's unknown vs any?",
         "any disables type checking — anything goes, no safety net. unknown is the type-safe counterpart — you MUST narrow the type before using it. Think: any = 'I don't care about types'. unknown = 'I don't know the type YET but I'll check before using it'.",
         "// any — no safety (avoid!)\nlet x: any = getData();\nx.foo.bar; // no error, might crash\n\n// unknown — must check first (safe)\nlet y: unknown = getData();\n// y.foo; // ERROR: Object is of type 'unknown'\n\nif (typeof y === 'string') {\n  y.toUpperCase(); // OK — narrowed to string\n}\n\nif (y instanceof User) {\n  y.name; // OK — narrowed to User\n}",
         "Use unknown for values from external sources (APIs, user input). Never use any unless migrating JS."),

        ("ADVANCED", 3, "Explain TypeScript discriminated unions.",
         "A pattern where a union of types shares a common literal property (the discriminant) that TypeScript uses to narrow the type. Think of it as a 'type tag' — switch on the tag and TypeScript knows exactly which shape you're dealing with. Essential for Redux actions, API responses, and state machines.",
         "type Shape =\n  | { kind: 'circle'; radius: number }\n  | { kind: 'rect'; w: number; h: number }\n  | { kind: 'triangle'; base: number; height: number };\n\nfunction area(s: Shape): number {\n  switch (s.kind) {\n    case 'circle':   return Math.PI * s.radius ** 2;\n    case 'rect':     return s.w * s.h;\n    case 'triangle': return 0.5 * s.base * s.height;\n  }\n}",
         "The 'kind' field is the discriminant. TypeScript auto-narrows inside each case branch."),

        ("ADVANCED", 3, "What is the TypeScript satisfies operator?",
         "satisfies (TS 4.9+) validates that a value matches a type WITHOUT widening the type. Unlike 'as', it preserves the narrowest inferred type while still type-checking. It catches errors at the assignment site, not at the usage site.",
         "type Color = 'red' | 'green' | 'blue';\ntype Theme = Record<string, Color | Color[]>;\n\n// With 'satisfies' — keeps literal types\nconst palette = {\n  primary: 'red',\n  secondary: ['green', 'blue'],\n} satisfies Theme;\n\npalette.primary.toUpperCase(); // OK — knows it's string\npalette.secondary.map(c => c); // OK — knows it's array\n\n// With 'as Theme' — loses specificity\n// palette.secondary.map() would error",
         "Use satisfies for config objects where you want validation AND narrow type inference."),

        ("ADVANCED", 3, "Explain JavaScript memory management and garbage collection.",
         "JS uses automatic garbage collection with a mark-and-sweep algorithm. Starting from roots (global, stack), it marks all reachable objects and sweeps (frees) unreachable ones. Memory leaks happen when references are kept alive unintentionally — they're never 'unreachable' so GC can't clean them.",
         "// LEAK: listener never removed\nfunction setup() {\n  const bigData = new Array(1e6).fill('x');\n  document.addEventListener('click', () => {\n    console.log(bigData.length); // bigData never GC'd\n  });\n}\n\n// FIX: remove listener\nconst handler = () => console.log('clicked');\ndocument.addEventListener('click', handler);\n// Cleanup:\ndocument.removeEventListener('click', handler);",
         "Common leak sources: forgotten listeners, closures over big data, global variables, detached DOM nodes."),

        ("ADVANCED", 3, "What is the JavaScript Proxy object?",
         "Proxy wraps an object and intercepts fundamental operations (get, set, delete, has, apply). It's like a middleware for object access. Combined with Reflect (which provides the default behavior), you can build reactive systems, validation layers, and logging. Vue 3's reactivity system is built on Proxy.",
         "const handler = {\n  get(target, key) {\n    console.log('Getting: ' + key);\n    return Reflect.get(target, key);\n  },\n  set(target, key, value) {\n    if (typeof value !== 'number')\n      throw new TypeError('Must be number');\n    return Reflect.set(target, key, value);\n  }\n};\nconst state = new Proxy({}, handler);\nstate.count = 5;  // validated\nstate.count;      // logs 'Getting: count'",
         "Proxy is how Vue 3 implements reactivity — understanding it is a strong senior signal."),

        ("ADVANCED", 3, "Explain JavaScript generators and iterators.",
         "Generator functions (function*) produce iterators via yield. They pause execution at each yield and resume on next(). This enables lazy evaluation (compute values only when needed), infinite sequences, and custom iteration protocols.",
         "function* range(start, end, step = 1) {\n  for (let i = start; i < end; i += step) yield i;\n}\nfor (const n of range(0, 10, 2)) {\n  console.log(n); // 0, 2, 4, 6, 8\n}\n\nfunction* fibonacci() {\n  let [a, b] = [0, 1];\n  while (true) { yield a; [a,b] = [b, a+b]; }\n}\nconst fib = fibonacci();\nfib.next().value; // 0\nfib.next().value; // 1",
         "Generators power async iteration (for await...of) and are the foundation of Redux-Saga."),

        ("ADVANCED", 2, "Explain Symbol and the iterator protocol.",
         "Symbol creates globally unique identifiers — even Symbol('foo') !== Symbol('foo'). Well-known symbols (Symbol.iterator, Symbol.toPrimitive) let you customize built-in behavior. The iterator protocol: any object with a [Symbol.iterator]() method returning {next()} is iterable with for...of.",
         "// Custom iterable\nclass Range {\n  constructor(start, end) {\n    this.start = start; this.end = end;\n  }\n  [Symbol.iterator]() {\n    let current = this.start;\n    const end = this.end;\n    return {\n      next() {\n        return current <= end\n          ? { value: current++, done: false }\n          : { done: true };\n      }\n    };\n  }\n}\n\nfor (const n of new Range(1, 5)) console.log(n);",
         "Making your classes iterable unlocks for...of, spread, destructuring, and Array.from()."),
    ],

    # =====================================================================
    "Phase 2: React & Next.js": [
        ("BASIC", 5, "What is the Virtual DOM?",
         "The Virtual DOM is a lightweight JavaScript copy of the real DOM. On every state change, React creates a new virtual tree, diffs it against the previous one (reconciliation), and updates ONLY the changed nodes in the real DOM. This batching makes updates efficient — like sending one package instead of many small ones.",
         "// React handles diffing automatically:\nfunction Counter() {\n  const [n, setN] = useState(0);\n  return (\n    <button onClick={() => setN(c => c+1)}>\n      Count: {n}\n    </button>\n  );\n  // Only the text node updates, not the whole button",
         "React's diffing algorithm assumes same-type elements at the same position are the same component."),

        ("BASIC", 5, "What is the difference between controlled and uncontrolled components?",
         "Controlled: React state is the single source of truth — value is driven by state, every keystroke fires onChange. Uncontrolled: the DOM is the source of truth, accessed via refs. Controlled is preferred for validation, conditional logic, and real-time formatting.",
         "// Controlled\nfunction Controlled() {\n  const [val, setVal] = useState('');\n  return (\n    <input\n      value={val}\n      onChange={e => setVal(e.target.value)}\n    />\n  );\n}\n\n// Uncontrolled\nfunction Uncontrolled() {\n  const ref = useRef();\n  const submit = () => console.log(ref.current.value);\n  return <input ref={ref} />;\n}",
         "File inputs are always uncontrolled — their value is read-only in the DOM."),

        ("BASIC", 5, "What is the difference between useEffect and useLayoutEffect?",
         "useEffect runs AFTER the browser paints — async, non-blocking, preferred for most side effects. useLayoutEffect runs BEFORE the browser paints — synchronous, blocks rendering. Use useLayoutEffect only when you need to read/mutate layout to avoid visual flickering.",
         "// useEffect — after paint (async, no flicker risk)\nuseEffect(() => {\n  document.title = 'Updated: ' + count;\n}, [count]);\n\n// useLayoutEffect — before paint (sync)\nuseLayoutEffect(() => {\n  const { height } = ref.current.getBoundingClientRect();\n  setHeight(height); // set before user sees anything\n}, []);",
         "Only reach for useLayoutEffect when you see visual flickering with useEffect."),

        ("BASIC", 5, "What role do keys play in React lists?",
         "Keys are React's identity system for list items. During reconciliation, React uses keys to match old and new elements. Bad keys (array index) cause state bugs when items reorder. Good keys (stable unique IDs) let React correctly track additions, removals, and reordering.",
         "// Bad — using index as key\nitems.map((item, i) => <Item key={i} data={item} />);\n// If items reorder, React thinks content\n// changed in place — local state is wrong\n\n// Good — stable unique ID\nitems.map(item => (\n  <Item key={item.id} data={item} />\n));",
         "Keys must be stable across renders, unique among siblings, and not randomly generated at render time."),

        ("INTERMEDIATE", 5, "Explain useMemo and useCallback — when to use them.",
         "useMemo memoizes a computed VALUE — recomputes only when deps change. useCallback memoizes a FUNCTION reference — creates new function only when deps change. Both exist to prevent expensive recalculations or child re-renders. But they have overhead too — don't use prematurely.",
         "// useMemo — skip re-sorting on unrelated renders\nconst sorted = useMemo(\n  () => [...items].sort((a,b) => a.price - b.price),\n  [items]\n);\n\n// useCallback — stable ref for memo'd child\nconst handleClick = useCallback(\n  () => dispatch({ type: 'INCREMENT' }),\n  [dispatch]\n);\n\n<ExpensiveChild onClick={handleClick} />",
         "useMemo/useCallback have overhead too. Add them only after profiling shows a real problem."),

        ("INTERMEDIATE", 5, "How does React Context API work? What are its limitations?",
         "Context passes data through the component tree without prop drilling. Create → Provider → useContext. The big limitation: ANY change to the Provider value re-renders ALL consumers — even those not using the changed value. For high-frequency state, use Zustand/Redux instead.",
         "const ThemeCtx = createContext('light');\n\nfunction App() {\n  const [theme, setTheme] = useState('light');\n  return (\n    <ThemeCtx.Provider value={{ theme, setTheme }}>\n      <Layout />\n    </ThemeCtx.Provider>\n  );\n}\n\nfunction Button() {\n  const { theme } = useContext(ThemeCtx);\n  return <button className={theme}>Click</button>;\n}",
         "Split context by concern — separate ThemeContext from UserContext to avoid unnecessary re-renders."),

        ("INTERMEDIATE", 5, "How do you prevent unnecessary re-renders?",
         "6 techniques: 1) React.memo — skip re-render if props unchanged. 2) useCallback — stable function refs. 3) useMemo — memoize derived values. 4) State colocation — keep state close to where it's used. 5) Context splitting — separate fast from slow context. 6) Virtualize long lists (react-window).",
         "// React.memo\nconst Card = React.memo(({ user }) => (\n  <div>{user.name}</div>\n));\n\n// Colocate state — don't lift unnecessarily\nfunction Form() {\n  // This state only affects Form\n  const [value, setValue] = useState('');\n  return <input value={value} onChange={e => setValue(e.target.value)} />;\n}",
         "Use React DevTools Profiler to identify what's actually re-rendering before optimizing."),

        ("INTERMEDIATE", 5, "Explain Next.js rendering: SSR, SSG, ISR, CSR.",
         "4 rendering strategies: SSR (Server-Side Rendering) — HTML generated per request, always fresh. SSG (Static Site Generation) — built at compile time, fastest. ISR (Incremental Static Regeneration) — SSG that auto-refreshes on a timer. CSR (Client-Side Rendering) — rendered in browser, used behind auth.",
         "// SSG (force-cache = static)\nasync function Page() {\n  const data = await fetch(url, { cache: 'force-cache' });\n  return <Render data={data} />;\n}\n\n// ISR — revalidate every 60 seconds\nasync function Page() {\n  const data = await fetch(url, { next: { revalidate: 60 } });\n  return <Render data={data} />;\n}\n\n// SSR — always fresh\nasync function Page() {\n  const data = await fetch(url, { cache: 'no-store' });\n  return <Render data={data} />;\n}",
         "ISR is the default recommendation for most marketing and content pages."),

        ("INTERMEDIATE", 5, "What is the difference between Server Components and Client Components?",
         "Server Components (default in App Router) run on the server — zero JS sent to browser, can access DB directly, but no hooks or browser APIs. Client Components ('use client') run in the browser — full React with hooks and events, but add to JS bundle. Push 'use client' as low as possible.",
         "'use client';\nimport { useState } from 'react';\n\n// Client Component\nexport function Counter() {\n  const [n, setN] = useState(0);\n  return <button onClick={() => setN(n+1)}>{n}</button>;\n}\n\n// Server Component (no directive)\nasync function UserList() {\n  const users = await db.user.findMany();\n  return users.map(u => <li key={u.id}>{u.name}</li>);\n}",
         "Server Components reduce JS bundle size. Push 'use client' as far down the tree as possible."),

        ("INTERMEDIATE", 5, "Explain Suspense and Error Boundaries.",
         "Suspense shows fallback UI while async content loads (like a loading spinner). Error Boundaries catch JS errors in child components and show fallback UI instead of crashing the whole app. Together they create resilient UIs that handle loading and error states gracefully.",
         "// Suspense — loading state\n<Suspense fallback={<Spinner />}>\n  <UserProfile /> {/* async component */}\n</Suspense>\n\n// Error Boundary (class component)\nclass ErrorBoundary extends React.Component {\n  state = { hasError: false };\n  static getDerivedStateFromError(error) {\n    return { hasError: true };\n  }\n  render() {\n    if (this.state.hasError)\n      return <h2>Something went wrong.</h2>;\n    return this.props.children;\n  }\n}",
         "Nest Suspense boundaries: coarse for layout, fine-grained for individual data sections."),

        ("INTERMEDIATE", 5, "How do you write custom hooks?",
         "Custom hooks extract reusable stateful logic into a function starting with 'use'. They can call other hooks. They share logic, not state — each component using the hook gets its own state. This is the primary way to reuse logic in functional React.",
         "function useLocalStorage(key, initialValue) {\n  const [value, setValue] = useState(() => {\n    const stored = localStorage.getItem(key);\n    return stored ? JSON.parse(stored) : initialValue;\n  });\n\n  useEffect(() => {\n    localStorage.setItem(key, JSON.stringify(value));\n  }, [key, value]);\n\n  return [value, setValue];\n}\n\n// Usage\nconst [theme, setTheme] = useLocalStorage('theme', 'dark');",
         "Name custom hooks with 'use' prefix — React's linter relies on this to check hook rules."),

        ("INTERMEDIATE", 4, "Explain useReducer and when to prefer it over useState.",
         "useReducer manages complex state via a pure reducer function (state + action → new state). Prefer it when: state has multiple interrelated sub-values, transitions are complex, or you want testable logic separate from the component. It's like a mini Redux inside your component.",
         "type Action =\n  | { type: 'INCREMENT' }\n  | { type: 'DECREMENT' }\n  | { type: 'RESET' };\n\nfunction reducer(state: number, action: Action) {\n  switch (action.type) {\n    case 'INCREMENT': return state + 1;\n    case 'DECREMENT': return state - 1;\n    case 'RESET': return 0;\n    default: return state;\n  }\n}\n\nconst [count, dispatch] = useReducer(reducer, 0);\ndispatch({ type: 'INCREMENT' });",
         "useReducer + Context is a lightweight alternative to Redux for medium complexity."),

        ("INTERMEDIATE", 4, "Compare state management: Redux vs Zustand vs Jotai.",
         "Redux: predictable, verbose, mature ecosystem, best for large teams with complex state. Zustand: simple API (no boilerplate), uses hooks, great for medium apps. Jotai: atom-based (bottom-up), minimal re-renders, great for derived/async state. Pick based on team size and complexity.",
         "// Zustand — simplest API\nconst useStore = create((set) => ({\n  count: 0,\n  inc: () => set((s) => ({ count: s.count + 1 })),\n}));\nfunction Counter() {\n  const count = useStore((s) => s.count);\n  const inc = useStore((s) => s.inc);\n  return <button onClick={inc}>{count}</button>;\n}\n\n// Jotai — atom-based\nconst countAtom = atom(0);\nconst [count, setCount] = useAtom(countAtom);",
         "Start with useState → useReducer → Zustand → Redux. Don't over-engineer state management."),

        ("INTERMEDIATE", 4, "Explain useTransition and useDeferredValue.",
         "Both handle non-urgent updates without blocking the UI. useTransition: wraps a state update as low-priority — shows old content while computing new. useDeferredValue: creates a deferred copy of a value that updates on a delay. Both keep the UI responsive during expensive renders.",
         "// useTransition — non-blocking state update\nfunction Search() {\n  const [query, setQuery] = useState('');\n  const [isPending, startTransition] = useTransition();\n  const [results, setResults] = useState([]);\n\n  function handleChange(e) {\n    setQuery(e.target.value); // urgent\n    startTransition(() => {\n      setResults(filterData(e.target.value)); // deferred\n    });\n  }\n  return <>{isPending && <Spinner />}</>;\n}",
         "useTransition for state updates you control. useDeferredValue for values from props/parent."),

        ("INTERMEDIATE", 4, "What are React Server Actions?",
         "Server Actions (React 19 / Next.js 14+) let you define server-side functions that can be called directly from Client Components. They replace API routes for form submissions and mutations. Mark with 'use server' and use with form action={} or call programmatically.",
         "// app/actions.ts\n'use server';\nexport async function createPost(formData: FormData) {\n  const title = formData.get('title');\n  await db.post.create({ data: { title } });\n  revalidatePath('/posts');\n}\n\n// app/page.tsx\nimport { createPost } from './actions';\nexport default function Page() {\n  return (\n    <form action={createPost}>\n      <input name='title' />\n      <button type='submit'>Create</button>\n    </form>\n  );\n}",
         "Server Actions eliminate the need for separate API routes for mutations in Next.js."),

        ("INTERMEDIATE", 4, "Explain Next.js App Router vs Pages Router.",
         "Pages Router (legacy): file-based routing in /pages, uses getServerSideProps/getStaticProps, no Server Components. App Router (modern): file-based in /app, Server Components by default, layouts, loading.tsx, error.tsx, streaming, and parallel routes. App Router is the future.",
         "// Pages Router (old)\n// pages/about.tsx\nexport async function getServerSideProps() {\n  const data = await fetchData();\n  return { props: { data } };\n}\nexport default function About({ data }) { ... }\n\n// App Router (new)\n// app/about/page.tsx\nexport default async function About() {\n  const data = await fetchData(); // direct await!\n  return <div>{data.title}</div>;\n}\n// app/about/loading.tsx → auto Suspense\n// app/about/error.tsx → auto Error Boundary",
         "New projects should always use App Router. Migrate existing Pages Router incrementally."),

        ("INTERMEDIATE", 4, "What are hydration errors and how do you fix them?",
         "Hydration errors occur when server-rendered HTML doesn't match client-rendered output. React expects the initial client render to exactly match the server HTML. Common causes: using Date.now(), window checks, random values, or browser-only APIs during initial render.",
         "// BAD — different on server vs client\nfunction Clock() {\n  return <p>{new Date().toLocaleString()}</p>;\n}\n\n// FIX — render only on client\nfunction Clock() {\n  const [time, setTime] = useState('');\n  useEffect(() => {\n    setTime(new Date().toLocaleString());\n  }, []);\n  return <p>{time}</p>;\n}\n\n// Or suppress hydration warning (last resort)\n<p suppressHydrationWarning>\n  {new Date().toLocaleString()}\n</p>",
         "Server and client must produce identical initial HTML. Use useEffect for client-only values."),

        ("INTERMEDIATE", 3, "Explain Next.js caching layers.",
         "Next.js has 4 cache layers: 1) Request Memoization — dedup same fetch in one render. 2) Data Cache — persists fetch results across requests (revalidate to refresh). 3) Full Route Cache — caches rendered HTML for static pages. 4) Router Cache — caches visited routes in the browser for instant back/forward.",
         "// Opt out of Data Cache (fresh every request)\nfetch(url, { cache: 'no-store' });\n\n// Revalidate every 60 seconds\nfetch(url, { next: { revalidate: 60 } });\n\n// On-demand revalidation\nimport { revalidatePath, revalidateTag } from 'next/cache';\nawait revalidatePath('/products');\nawait revalidateTag('products');\n\n// Tag a fetch for targeted revalidation\nfetch(url, { next: { tags: ['products'] } });",
         "Understand all 4 cache layers to debug 'why isn't my data updating?' — the #1 Next.js question."),

        ("INTERMEDIATE", 3, "What is React 19's use() hook?",
         "use() reads the value of a Promise or Context during render. Unlike useContext, it can be called conditionally. Unlike await, it integrates with Suspense — the component suspends while the promise resolves. It replaces many useEffect-for-data-fetching patterns.",
         "import { use, Suspense } from 'react';\n\nfunction UserProfile({ userPromise }) {\n  const user = use(userPromise); // suspends!\n  return <h1>{user.name}</h1>;\n}\n\n// Conditional context (not possible with useContext)\nfunction Theme({ showTheme }) {\n  if (showTheme) {\n    const theme = use(ThemeContext);\n    return <p>{theme}</p>;\n  }\n  return null;\n}",
         "use() can be called inside if/else blocks — the only hook that breaks the 'no conditional hooks' rule."),

        ("INTERMEDIATE", 3, "Explain React ref forwarding and useImperativeHandle.",
         "forwardRef passes a ref from parent to a child's internal DOM element. useImperativeHandle customizes what the ref exposes — instead of the raw DOM node, you expose specific methods. This creates clean component APIs while hiding implementation details.",
         "const FancyInput = forwardRef((props, ref) => {\n  const inputRef = useRef();\n\n  useImperativeHandle(ref, () => ({\n    focus: () => inputRef.current.focus(),\n    clear: () => { inputRef.current.value = ''; },\n  }));\n\n  return <input ref={inputRef} {...props} />;\n});\n\n// Parent\nconst ref = useRef();\n<FancyInput ref={ref} />\nref.current.focus(); // calls exposed method\nref.current.clear(); // works too",
         "useImperativeHandle lets you expose only what's needed — better encapsulation than raw refs."),

        ("ADVANCED", 5, "Explain Next.js Middleware and its use cases.",
         "Middleware runs on the Edge BEFORE any page renders — can redirect, rewrite URLs, set headers, and check auth. It executes at CDN edge nodes globally with near-zero latency. Perfect for auth guards, A/B testing, geolocation routing, and i18n redirects.",
         "// middleware.ts\nimport { NextResponse } from 'next/server';\nimport type { NextRequest } from 'next/server';\n\nexport function middleware(req: NextRequest) {\n  const token = req.cookies.get('token');\n  if (!token &&\n    req.nextUrl.pathname.startsWith('/dashboard')) {\n    return NextResponse.redirect(\n      new URL('/login', req.url)\n    );\n  }\n  return NextResponse.next();\n}\n\nexport const config = {\n  matcher: ['/dashboard/:path*'],\n};",
         "Middleware runs on the Edge Runtime — limited to Web APIs (no Node.js fs, child_process, etc.)."),

        ("ADVANCED", 4, "How do you implement code splitting in Next.js?",
         "Next.js automatically code-splits by page. For component-level splitting, use next/dynamic (which wraps React.lazy + Suspense). Use ssr: false for browser-only components (charts, maps, editors). This reduces initial bundle size dramatically.",
         "import dynamic from 'next/dynamic';\n\n// Heavy chart only loaded when rendered\nconst Chart = dynamic(\n  () => import('../components/Chart'),\n  {\n    loading: () => <p>Loading chart...</p>,\n    ssr: false, // browser-only component\n  }\n);\n\nexport default function Dashboard() {\n  return (\n    <main>\n      <h1>Dashboard</h1>\n      <Chart data={data} />\n    </main>\n  );\n}",
         "Use ssr: false for components using window, document, or other browser-only APIs."),

        ("ADVANCED", 4, "How would you implement authentication in Next.js?",
         "Best practice: use Auth.js (NextAuth). For custom: store JWT in httpOnly cookies (not localStorage — XSS-safe). Use Middleware to protect routes globally. Server Components read cookies directly; Client Components use a session hook or Server Actions.",
         "// Route handler — login\nexport async function POST(req: Request) {\n  const { email, password } = await req.json();\n  const user = await validateUser(email, password);\n  if (!user)\n    return Response.json({ error: 'Unauthorized' }, { status: 401 });\n\n  const token = signJWT({ id: user.id, role: user.role });\n  const res = Response.json({ ok: true });\n  res.headers.set('Set-Cookie',\n    `token=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=3600`\n  );\n  return res;\n}",
         "Never store JWTs in localStorage — they are vulnerable to XSS attacks. Always use httpOnly cookies."),

        ("ADVANCED", 4, "Explain Next.js generateMetadata for dynamic SEO.",
         "generateMetadata is an async function that generates page-specific meta tags (title, description, Open Graph, Twitter cards) at the route level. It can fetch data to build dynamic metadata. This is essential for SEO in dynamic pages.",
         "// app/products/[id]/page.tsx\nexport async function generateMetadata({ params }) {\n  const product = await getProduct(params.id);\n  return {\n    title: product.name + ' | MyStore',\n    description: product.description.slice(0, 160),\n    openGraph: {\n      title: product.name,\n      images: [product.image],\n    },\n    twitter: {\n      card: 'summary_large_image',\n    },\n  };\n}\n\nexport default async function ProductPage({ params }) {\n  const product = await getProduct(params.id);\n  return <ProductView product={product} />;\n}",
         "generateMetadata runs on the server and deduplicates data fetching with the page component."),

        ("ADVANCED", 4, "What are Web Vitals (LCP, CLS, INP) and why are they important?",
         "Core Web Vitals are Google's user experience metrics that directly impact SEO rankings. LCP (Largest Contentful Paint) < 2.5s — loading speed. CLS (Cumulative Layout Shift) < 0.1 — visual stability. INP (Interaction to Next Paint) < 200ms — responsiveness.",
         "import { useReportWebVitals } from 'next/web-vitals'\n\nexport function WebVitals() {\n  useReportWebVitals((metric) => {\n    if (metric.name === 'LCP') {\n      console.log('LCP:', metric.value);\n      // Send to analytics\n    }\n  })\n}",
         "Next.js optimizes these automatically via next/image (CLS/LCP), next/font (CLS), and Server Components (INP)."),

        ("ADVANCED", 3, "What are React 19's useOptimistic and useFormStatus?",
         "useOptimistic shows optimistic UI updates immediately while the server processes. useFormStatus gives pending state of a parent form — useful for showing loading in submit buttons. Both eliminate common boilerplate for form interactions.",
         "// useOptimistic\nfunction Todos({ todos, addTodo }) {\n  const [optimistic, addOptimistic] = useOptimistic(\n    todos,\n    (state, newTodo) => [...state, { ...newTodo, pending: true }]\n  );\n  async function handleAdd(formData) {\n    addOptimistic({ text: formData.get('text') });\n    await addTodo(formData); // server action\n  }\n}\n\n// useFormStatus\nfunction SubmitButton() {\n  const { pending } = useFormStatus();\n  return <button disabled={pending}>\n    {pending ? 'Saving...' : 'Save'}\n  </button>;\n}",
         "useOptimistic makes apps feel instant — update UI first, then confirm with server."),

        ("ADVANCED", 3, "Explain Next.js Parallel Routes and Intercepting Routes.",
         "Parallel Routes (@slot convention) render multiple pages simultaneously in the same layout — like dashboards with independent panels. Intercepting Routes ((..) convention) show a route in a modal while preserving the underlying page — like Instagram's photo modal on feed.",
         "// Parallel Routes\n// app/layout.tsx\nexport default function Layout({ children, analytics, team }) {\n  return (\n    <>\n      {children}\n      {analytics}  {/* @analytics/page.tsx */}\n      {team}       {/* @team/page.tsx */}\n    </>\n  );\n}\n// Each slot loads independently + has its own loading/error\n\n// Intercepting Routes\n// app/feed/(..)photo/[id]/page.tsx\n// Shows photo in modal when navigating from /feed\n// Direct URL /photo/[id] shows full page",
         "Parallel Routes are perfect for dashboards. Intercepting Routes for modal-based navigation."),

        ("ADVANCED", 3, "Explain the React 19 Compiler (React Forget) and how it changes memoization.",
         "The React 19 Compiler (formerly React Forget) is an auto-memoization compiler. It compiles React code to automatically insert the equivalent of useMemo and useCallback. This eliminates the need for developers to manually manage dependency arrays and optimizes render performance by default. It guarantees component and hook values are only re-computed when their inputs actually change.",
         "// Before: Manual memoization\nconst MemoizedList = React.memo(({ items }) => {\n  const sorted = useMemo(() => items.sort(), [items]);\n  const onClick = useCallback(() => {}, []);\n  return <div onClick={onClick}>{sorted.join(', ')}</div>;\n});\n\n// After: Just normal code, the compiler handles memoization!\nconst List = ({ items }) => {\n  const sorted = items.sort();\n  const onClick = () => {};\n  return <div onClick={onClick}>{sorted.join(', ')}</div>;\n}",
         "The compiler makes manual useMemo and useCallback obsolete in most cases, but you still need them for custom hook stability if not using the compiler yet."),

        ("ADVANCED", 4, "Explain the React Server Component (RSC) payload and how serialization works.",
         "The RSC payload is a compact, serialized representation of the React component tree returned from the server to the client. It contains the rendered virtual DOM structure, resolved props, and references to Client Component files (client references). Because this payload is sent over the network, all props passed from Server Components to Client Components must be serializable (no functions, classes, or symbols).",
         "// Server Component\nasync function ServerPage() {\n  const data = await db.fetch();\n  // data is serialized to JSON-like structure in RSC payload\n  return <ClientButton data={data} />;\n}\n\n// RSC payload includes:\n// M1:client-reference-to-ClientButton.js\n// J0:[\"div\",null,[\"h1\",null,\"Title\"],[\"$@M1\",{\"data\":{\"id\":1}}]]",
         "If you pass a function or non-serializable object across the server-client boundary, React will throw a serialization error."),

        ("ADVANCED", 4, "Explain the security features of React 19 Server Actions.",
         "React 19 Server Actions are secure endpoints by default. They include: 1) Automatic CSRF protection (checks Origin headers on requests), 2) Closed-over variable encryption (variables in action closure are encrypted before sending to the client so they cannot be inspected or tampered with), 3) Safe action exports (Next.js automatically generates random, unpredictable action URLs so they cannot be guessed).",
         "// app/actions.ts\n'use server';\n\nexport async function deleteUser(id: string) {\n  // 1. origin header verified to prevent CSRF\n  // 2. 'id' is verified and validated\n  // 3. User authorization must still be checked manually!\n  const session = await getSession();\n  if (session?.user.role !== 'admin') throw new Error('Unauthorized');\n  await db.user.delete(id);\n}",
         "Even with Server Actions security, you must still perform authentication and authorization checks inside the action body."),

        ("ADVANCED", 3, "How do you implement a Multi-Zone architecture in Next.js?",
         "Multi-Zone allows you to merge multiple independently deployed Next.js applications into a single domain (e.g. /blog on one app, /dashboard on another). You configure this in next.config.js using rewrites to forward requests from the main app (the gateway) to the independent zone apps. This is ideal for large organizations where separate teams own separate sections of the site.",
         "// next.config.js (Main App / Gateway)\nmodule.exports = {\n  async rewrites() {\n    return [\n      {\n        source: '/blog',\n        destination: 'https://blog-zone.internal/blog',\n      },\n      {\n        source: '/blog/:path*',\n        destination: 'https://blog-zone.internal/blog/:path*',\n      },\n    ];\n  },\n};",
         "Ensure assets and CSS paths do not conflict by using unique basePath settings in each sub-app's config."),

        ("ADVANCED", 4, "Explain how Server-Sent Events (SSE) and Streaming work in Next.js Route Handlers.",
         "Streaming in Next.js leverages HTTP chunked transfer encoding, allowing the server to stream parts of the UI (via Suspense) or raw data (like AI responses) as they become available. For raw text/AI response streaming, you return a Response object initialized with a ReadableStream from a Route Handler. This is crucial for AI chat interfaces (e.g., ChatGPT style streaming).",
         "// app/api/chat/route.ts\nexport async function POST(req: Request) {\n  const encoder = new TextEncoder();\n  const stream = new ReadableStream({\n    async start(controller) {\n      for (let i = 0; i < 5; i++) {\n        controller.enqueue(encoder.encode(`Chunk ${i}\\n`));\n        await new Promise(r => setTimeout(r, 1000));\n      }\n      controller.close();\n    }\n  });\n  return new Response(stream, {\n    headers: { 'Content-Type': 'text/event-stream' }\n  });\n}",
         "Streaming reduces Time to First Byte (TTFB) and allows you to render static layouts while slow data streams in."),
    ],

    # =====================================================================
    "Phase 3: Node.js & Express": [
        ("BASIC", 5, "How does Node.js handle async if it is single-threaded?",
         "Node.js delegates heavy work (file I/O, network, crypto) to libuv's thread pool and the OS kernel. The single-threaded event loop continuously checks for completed operations and fires callbacks. This is why Node handles thousands of concurrent connections efficiently — it never blocks waiting.",
         "const fs = require('fs');\n\n// Non-blocking — delegates to OS\nfs.readFile('large.txt', 'utf8', (err, data) => {\n  // Runs when I/O completes\n  console.log('Done:', data.length);\n});\n\nconsole.log('Runs first — sync'); // runs immediately",
         "CPU-bound tasks block the event loop — use worker_threads or child_process for those."),

        ("BASIC", 5, "What is Express middleware and how does it work?",
         "Middleware are functions in a pipeline — each receives req, res, and next(). They execute in order, can modify request/response, and pass control via next(). Think of it as an assembly line: each station does its job and passes the product forward. Order matters!",
         "const app = express();\n\n// Logger middleware\napp.use((req, res, next) => {\n  console.log(req.method + ' ' + req.path);\n  next();\n});\n\n// Auth middleware\napp.use('/api', requireAuth);\n\n// Error handler (4 params — must be last)\napp.use((err, req, res, next) => {\n  res.status(500).json({ error: err.message });\n});",
         "Error-handling middleware MUST have exactly 4 parameters (err, req, res, next) to work."),

        ("BASIC", 5, "What is CORS and how do you configure it?",
         "CORS (Cross-Origin Resource Sharing) is a browser security mechanism that blocks requests from different origins by default. The server must explicitly whitelist allowed origins, methods, and headers. Without proper CORS, your frontend can't talk to your backend on a different domain.",
         "const cors = require('cors');\n\n// Allow specific origin (production)\napp.use(cors({\n  origin: 'https://myapp.com',\n  methods: ['GET', 'POST', 'PUT', 'DELETE'],\n  credentials: true,\n  allowedHeaders: ['Content-Type', 'Authorization'],\n}));\n\n// Multiple origins\nconst allowedOrigins = ['https://myapp.com', 'https://admin.myapp.com'];\napp.use(cors({\n  origin: (origin, callback) => {\n    if (!origin || allowedOrigins.includes(origin))\n      callback(null, true);\n    else callback(new Error('CORS blocked'));\n  },\n}));",
         "Never use cors() with no options in production — it allows ALL origins. Always whitelist."),

        ("INTERMEDIATE", 5, "How do you structure a large Node.js application?",
         "Layered architecture: Routes (HTTP layer) → Controllers (req/res handling) → Services (business logic) → Repositories/Models (data access). Each layer only talks to the one below. This separation makes code testable, maintainable, and mockable.",
         "// routes/user.routes.ts\nrouter.post('/users',\n  validate(createUserSchema),\n  userController.create\n);\n\n// controllers/user.controller.ts\nasync create(req, res, next) {\n  try {\n    const user = await userService.create(req.body);\n    res.status(201).json(user);\n  } catch(e) { next(e); }\n}\n\n// services/user.service.ts\nasync create(data) {\n  await this.verifyEmailUnique(data.email);\n  return userRepository.save(data);\n}",
         "Never put business logic in controllers or routes — it kills testability."),

        ("INTERMEDIATE", 5, "Explain JWT authentication flow.",
         "5-step dance: 1) User submits credentials. 2) Server validates and signs a JWT with a secret. 3) Client stores and sends it in Authorization header. 4) Server verifies the token on protected routes. 5) Use short-lived access tokens (15min) + long-lived refresh tokens (7-30 days in httpOnly cookies).",
         "// Sign on login\nconst token = jwt.sign(\n  { userId: user.id, role: user.role },\n  process.env.JWT_SECRET,\n  { expiresIn: '15m' }\n);\n\n// Verify middleware\nfunction authenticate(req, res, next) {\n  const token = req.headers.authorization?.split(' ')[1];\n  if (!token) return res.status(401).json({ error: 'No token' });\n  try {\n    req.user = jwt.verify(token, process.env.JWT_SECRET);\n    next();\n  } catch { res.status(401).json({ error: 'Invalid token' }); }\n}",
         "Access token: 15 min in memory/header. Refresh token: 7-30 days in httpOnly cookie."),

        ("INTERMEDIATE", 5, "How do you handle errors globally in Express?",
         "Three-part strategy: 1) Custom error classes with status codes. 2) Async wrapper (catchAsync) to forward promise rejections. 3) Centralized error handler as the LAST middleware. Never send stack traces to clients in production.",
         "// Custom error class\nclass AppError extends Error {\n  constructor(message, statusCode) {\n    super(message);\n    this.statusCode = statusCode;\n  }\n}\n\n// Async wrapper — catches promise rejections\nconst catchAsync = fn =>\n  (req, res, next) =>\n    Promise.resolve(fn(req, res, next)).catch(next);\n\n// Global handler\napp.use((err, req, res, next) => {\n  const status = err.statusCode || 500;\n  res.status(status).json({\n    error: err.message,\n    ...(process.env.NODE_ENV !== 'production'\n      && { stack: err.stack })\n  });\n});",
         "Express only catches sync errors automatically — always handle async with catchAsync or try/catch."),

        ("INTERMEDIATE", 4, "What is RBAC and how do you implement it in Express?",
         "Role-Based Access Control restricts API access based on user roles. Each role has a set of permissions. Middleware checks the user's role before granting access. This decouples authorization logic from business logic and makes it composable.",
         "const permissions = {\n  admin:  ['read','write','delete'],\n  editor: ['read','write'],\n  viewer: ['read'],\n};\n\nfunction authorize(...perms) {\n  return (req, res, next) => {\n    const userPerms = permissions[req.user.role] || [];\n    const allowed = perms.every(p => userPerms.includes(p));\n    if (!allowed)\n      return res.status(403).json({ error: 'Forbidden' });\n    next();\n  };\n}\n\nrouter.delete('/posts/:id',\n  authenticate,\n  authorize('delete'),\n  postController.delete\n);",
         "For complex permission systems, consider Casbin or OPA (Open Policy Agent)."),

        ("INTERMEDIATE", 4, "Explain process.nextTick() vs setImmediate().",
         "process.nextTick runs BEFORE the next event loop phase (highest priority microtask). setImmediate runs AFTER the current poll phase completes (next iteration). nextTick can starve I/O if overused because it always cuts the line. In practice: use setImmediate for deferring, nextTick for critical callbacks.",
         "// nextTick runs first\nsetImmediate(() => console.log('setImmediate'));\nprocess.nextTick(() => console.log('nextTick'));\n// Output: nextTick, setImmediate\n\n// Danger: recursive nextTick starves I/O\nfunction badIdea() {\n  process.nextTick(badIdea); // blocks everything!\n}\n\n// Safe: recursive setImmediate allows I/O\nfunction safe() {\n  setImmediate(safe); // I/O can interleave\n}",
         "Use setImmediate to yield to I/O. Use nextTick only when you need to run before any I/O."),

        ("INTERMEDIATE", 4, "How do you handle file uploads in Node.js?",
         "Use Multer middleware for multipart/form-data (file uploads). Configure storage (disk or memory), file size limits, and file type filters. For large files, stream directly to cloud storage (S3) instead of loading into memory.",
         "const multer = require('multer');\n\nconst storage = multer.diskStorage({\n  destination: (req, file, cb) => cb(null, 'uploads/'),\n  filename: (req, file, cb) => {\n    const unique = Date.now() + '-' + Math.round(Math.random() * 1E9);\n    cb(null, unique + '-' + file.originalname);\n  }\n});\n\nconst upload = multer({\n  storage,\n  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB\n  fileFilter: (req, file, cb) => {\n    if (file.mimetype.startsWith('image/')) cb(null, true);\n    else cb(new Error('Only images allowed'), false);\n  }\n});\n\napp.post('/avatar', upload.single('photo'), (req, res) => {\n  res.json({ url: '/uploads/' + req.file.filename });\n});",
         "For production, stream uploads directly to S3/GCS — never store files on the app server."),

        ("INTERMEDIATE", 4, "Explain the Node.js cluster module and worker threads.",
         "Cluster: forks multiple processes (one per CPU core) sharing the same port — each process has its own event loop and memory. Worker threads: share memory via SharedArrayBuffer — true multi-threading for CPU-intensive work. Use cluster for scaling HTTP servers, workers for CPU-bound tasks.",
         "// Cluster — scale HTTP server\nconst cluster = require('cluster');\nconst os = require('os');\n\nif (cluster.isPrimary) {\n  const cpus = os.cpus().length;\n  for (let i = 0; i < cpus; i++) cluster.fork();\n  cluster.on('exit', () => cluster.fork());\n} else {\n  app.listen(3000);\n}\n\n// Worker thread — CPU-intensive task\nconst { Worker } = require('worker_threads');\nconst worker = new Worker('./heavy-task.js');\nworker.on('message', result => console.log(result));",
         "In production, use PM2 in cluster mode instead of manual cluster management."),

        ("INTERMEDIATE", 4, "What are security headers and how do you set them?",
         "Security headers tell browsers how to protect your app. Helmet.js sets them automatically: Content-Security-Policy (blocks XSS), X-Frame-Options (prevents clickjacking), Strict-Transport-Security (forces HTTPS), X-Content-Type-Options (prevents MIME sniffing).",
         "const helmet = require('helmet');\napp.use(helmet()); // sets all security headers\n\n// Custom CSP\napp.use(helmet.contentSecurityPolicy({\n  directives: {\n    defaultSrc: [\"'self'\"],\n    scriptSrc: [\"'self'\", \"'unsafe-inline'\"],\n    styleSrc: [\"'self'\", \"fonts.googleapis.com\"],\n    imgSrc: [\"'self'\", \"data:\", \"cdn.example.com\"],\n    connectSrc: [\"'self'\", \"api.example.com\"],\n  }\n}));",
         "Always use Helmet in production. One line (app.use(helmet())) gives you major security improvements."),

        ("INTERMEDIATE", 4, "How do you implement graceful shutdown in Node.js?",
         "Graceful shutdown lets the server finish active requests before stopping — no dropped connections. Listen for SIGTERM/SIGINT, stop accepting new connections, wait for in-flight requests to complete, then close database pools and exit. Critical for zero-downtime deployments.",
         "process.on('SIGTERM', gracefulShutdown);\nprocess.on('SIGINT', gracefulShutdown);\n\nasync function gracefulShutdown(signal) {\n  console.log(`${signal} received. Shutting down...`);\n\n  // Stop accepting new connections\n  server.close(async () => {\n    console.log('HTTP server closed');\n\n    // Close DB connections\n    await db.end();\n    await redis.quit();\n\n    console.log('All connections closed');\n    process.exit(0);\n  });\n\n  // Force kill after 30 seconds\n  setTimeout(() => {\n    console.error('Forced shutdown');\n    process.exit(1);\n  }, 30000);\n}",
         "Kubernetes sends SIGTERM before killing pods — graceful shutdown prevents request failures."),

        ("INTERMEDIATE", 3, "Explain Node.js EventEmitter pattern.",
         "EventEmitter is Node's core pub/sub system — objects emit named events, listeners subscribe to them. It decouples producers from consumers. Most Node.js core modules (streams, http, fs) extend EventEmitter. It's the foundation of Node's event-driven architecture.",
         "const EventEmitter = require('events');\n\nclass OrderService extends EventEmitter {\n  async createOrder(data) {\n    const order = await db.orders.create(data);\n    this.emit('order:created', order);\n    return order;\n  }\n}\n\nconst orders = new OrderService();\n\n// Decoupled listeners\norders.on('order:created', order => {\n  emailService.sendConfirmation(order);\n});\norders.on('order:created', order => {\n  analyticsService.track('purchase', order);\n});",
         "EventEmitter is synchronous by default — listeners run in order, not in parallel."),

        ("INTERMEDIATE", 3, "Compare Express vs Fastify vs Hono.",
         "Express: most popular, huge ecosystem, callback-based, moderate performance. Fastify: 2-3x faster than Express, schema-based validation, built-in serialization, plugin architecture. Hono: ultralight, runs everywhere (Node, Deno, Bun, Edge, Workers), Web Standard APIs. Choose based on platform and performance needs.",
         "// Express\napp.get('/hello', (req, res) => {\n  res.json({ hello: 'world' });\n});\n\n// Fastify\nfastify.get('/hello', {\n  schema: {\n    response: { 200: { type: 'object',\n      properties: { hello: { type: 'string' }}}}\n  }\n}, async () => ({ hello: 'world' }));\n\n// Hono (edge-native)\nconst app = new Hono();\napp.get('/hello', (c) => c.json({ hello: 'world' }));",
         "Express for most projects. Fastify for high-performance APIs. Hono for edge/serverless."),

        ("ADVANCED", 4, "How do you implement rate limiting in a distributed Node.js system?",
         "express-rate-limit handles single-server limits. For distributed systems (multiple servers behind a load balancer), use Redis as a shared store so rate limits apply consistently across all instances. Apply stricter limits on auth routes to prevent brute-force attacks.",
         "const rateLimit = require('express-rate-limit');\nconst RedisStore = require('rate-limit-redis');\n\nconst limiter = rateLimit({\n  windowMs: 15 * 60 * 1000, // 15 minutes\n  max: 100,\n  standardHeaders: true,\n  store: new RedisStore({\n    client: redisClient,\n    prefix: 'rl:',\n  }),\n  keyGenerator: req => req.user?.id || req.ip,\n});\n\n// Stricter limit on auth routes\nconst authLimiter = rateLimit({\n  windowMs: 60 * 1000,\n  max: 5, // 5 attempts per minute\n});\n\napp.use('/api/', limiter);\napp.use('/api/auth/', authLimiter);",
         "Apply stricter limits on /login and /register to prevent brute-force attacks."),

        ("ADVANCED", 4, "Explain Node.js streams and when to use them.",
         "Streams process data in chunks rather than loading everything into memory. 4 types: Readable, Writable, Duplex (both), Transform (modify data as it passes). Critical for large files, video streaming, and data pipelines. A 2GB file doesn't need 2GB RAM — streams use constant memory.",
         "const fs = require('fs');\nconst zlib = require('zlib');\n\n// Stream large file through gzip compression\nfs.createReadStream('large.csv')\n  .pipe(zlib.createGzip())\n  .pipe(fs.createWriteStream('large.csv.gz'))\n  .on('finish', () => console.log('Compressed'));\n\n// Stream DB query results to HTTP response\napp.get('/export', (req, res) => {\n  res.setHeader('Content-Type', 'text/csv');\n  db.queryStream('SELECT * FROM orders')\n    .pipe(csvTransform)\n    .pipe(res);\n});",
         "Never use fs.readFile for large files — always stream them."),

        ("ADVANCED", 4, "How do you implement WebSockets for real-time features?",
         "WebSockets provide full-duplex persistent connections — the server can push data to clients instantly. Unlike HTTP polling (client asks repeatedly), WebSockets stay open. Use Socket.IO for production (handles reconnection, rooms, fallbacks). Scale across servers with Redis pub/sub adapter.",
         "const { Server } = require('socket.io');\nconst io = new Server(httpServer);\n\nio.on('connection', socket => {\n  socket.on('join-room', roomId => {\n    socket.join(roomId);\n    socket.to(roomId).emit('user-joined', socket.id);\n  });\n\n  socket.on('message', ({ roomId, text }) => {\n    io.to(roomId).emit('message', {\n      from: socket.id,\n      text,\n      at: new Date().toISOString()\n    });\n  });\n\n  socket.on('disconnect', () => {\n    console.log('Disconnected:', socket.id);\n  });\n});",
         "Use @socket.io/redis-adapter to sync events across multiple Node.js instances."),

        ("ADVANCED", 3, "How do you manage environment variables securely?",
         "Never hardcode secrets. Use .env files locally (dotenv), but in production use secret managers (AWS Secrets Manager, Vault). Validate all env vars at startup — fail fast if any are missing. Never commit .env to git.",
         "// Validate env vars at startup\nconst required = ['DATABASE_URL', 'JWT_SECRET', 'REDIS_URL'];\nfor (const key of required) {\n  if (!process.env[key])\n    throw new Error(`Missing required env var: ${key}`);\n}\n\n// Use a config module\nexport const config = {\n  port: parseInt(process.env.PORT || '3000'),\n  db: process.env.DATABASE_URL,\n  jwt: {\n    secret: process.env.JWT_SECRET,\n    expiresIn: process.env.JWT_EXPIRES || '15m',\n  },\n  isProduction: process.env.NODE_ENV === 'production',\n} as const;",
         "Use zod to validate env vars: z.object({ PORT: z.coerce.number() }).parse(process.env)."),

        ("ADVANCED", 3, "What is input validation and how do you implement it?",
         "Never trust client input — validate everything on the server. Use schema validation libraries (Zod, Joi, Yup) to define expected shapes and reject invalid data early. Validate in middleware before the request reaches controllers.",
         "const { z } = require('zod');\n\nconst createUserSchema = z.object({\n  name: z.string().min(2).max(100),\n  email: z.string().email(),\n  age: z.number().int().min(18).optional(),\n  role: z.enum(['user', 'admin']).default('user'),\n});\n\n// Validation middleware\nfunction validate(schema) {\n  return (req, res, next) => {\n    const result = schema.safeParse(req.body);\n    if (!result.success) {\n      return res.status(400).json({\n        errors: result.error.flatten().fieldErrors\n      });\n    }\n    req.body = result.data; // cleaned data\n    next();\n  };\n}\n\napp.post('/users', validate(createUserSchema), controller.create);",
         "Zod is the standard for TypeScript projects — it infers TypeScript types from schemas."),

        ("ADVANCED", 4, "Explain the phases of the Node.js Event Loop in detail.",
         "The event loop has six main phases: 1) Timers (executes setTimeout/setInterval callbacks), 2) Pending callbacks (executes I/O callbacks deferred from previous loop iteration), 3) Idle, prepare (internal use), 4) Poll (retrieves new I/O events; executes I/O-related callbacks), 5) Check (executes setImmediate callbacks), 6) Close callbacks (e.g., socket.on('close')). Between each phase, Node.js processes microtasks (Promises and process.nextTick).",
         "setTimeout(() => console.log('Timer'), 0);\nsetImmediate(() => console.log('Immediate'));\nprocess.nextTick(() => console.log('NextTick'));\nPromise.resolve().then(() => console.log('Promise'));\n\n// Output order:\n// 1. NextTick\n// 2. Promise\n// 3. Timer\n// 4. Immediate (depending on loop entrance timing)",
         "process.nextTick fires immediately after the current operation finishes, before event loop phases run."),

        ("ADVANCED", 4, "How do you detect and debug memory leaks in Node.js applications?",
         "Memory leaks happen when objects are kept in memory and not garbage collected. To debug: 1) Run Node with the --inspect flag, 2) Use Chrome DevTools or a tool like memlab to capture Heap Snapshots, 3) Perform actions to trigger the leak, 4) Take another snapshot and compare them (using 'Comparison' view to find growing object counts). Common culprits include global variables, forgotten event listeners, intervals, and closures.",
         "// Start node with inspect: node --inspect index.js\n// Programmatically triggering a heap snapshot:\nconst heapdump = require('heapdump');\n\nheapdump.writeSnapshot((err, filename) => {\n  console.log('Snapshot written to:', filename);\n});",
         "Check for growing array/object lengths stored outside request lifecycle context."),

        ("ADVANCED", 4, "What is AsyncLocalStorage and how is it used for request tracking?",
         "AsyncLocalStorage (from the node:async_hooks module) lets you store data throughout the lifetime of an asynchronous web request, similar to thread-local storage in multi-threaded languages. This is incredibly useful for passing request-scoped context (like a user ID or Correlation ID for logging) to deeply nested functions without explicitly passing it through every function argument (prop drilling).",
         "const { AsyncLocalStorage } = require('node:async_hooks');\nconst storage = new AsyncLocalStorage();\n\napp.use((req, res, next) => {\n  const requestId = req.headers['x-request-id'] || generateId();\n  storage.run({ requestId }, () => next());\n});\n\n// Deep in controller or DB layer:\nfunction logMessage(msg) {\n  const store = storage.getStore();\n  console.log(`[${store?.requestId || 'system'}] ${msg}`);\n}",
         "AsyncLocalStorage is standard in modern frameworks (like Next.js headers/cookies functions)."),

        ("ADVANCED", 3, "How do you implement structured logging and distributed tracing in Node.js?",
         "Structured logging uses JSON format instead of plain text, making logs easily searchable by log aggregators (Elasticsearch, Loki, Datadog). Use a fast logger like Pino or Winston. Combined with AsyncLocalStorage, you can inject a Correlation ID into every log statement inside the request lifecycle to trace requests across microservices.",
         "const pino = require('pino');\nconst logger = pino();\n\n// Structured log output:\n// {'level':30,'time':1623457,'msg':'User logged in','userId':123}\nlogger.info({ userId: 123 }, 'User logged in');\n\n// Downstream requests propagate correlation ID:\n// fetch('http://payment-service/pay', {\n//   headers: { 'X-Correlation-ID': correlationId }\n// });",
         "Never log sensitive data (passwords, credit cards) — use logger level sanitizers to filter them."),

        ("INTERMEDIATE", 3, "Explain package manager differences: npm vs yarn vs pnpm.",
         "npm/yarn v1 use flat node_modules, which leads to 'phantom dependencies' (packages using dependencies not declared in package.json due to hoisting) and slow, duplicate storage. pnpm solves this using a content-addressable store (files are stored once globally in ~/.pnpm-store and hard-linked into projects) and a nested node_modules structure using symlinks, which enforces dependency declaration strictly and saves disk space.",
         "# npm/Yarn v1: flat folder structure\n# node_modules/express, node_modules/accepts (hoisted!)\n\n# pnpm: symlinked nested folder structure\n# node_modules/express -> symlink to .pnpm/express@x.y.z/node_modules/express\n# Prevents code from importing 'accepts' unless explicitly declared.",
         "Use pnpm for faster installs, disk space savings, and to avoid phantom dependency bugs."),

        ("ADVANCED", 4, "How do you secure Node.js applications against OWASP Top 10 vulnerabilities?",
         "1) Prototype Pollution: freeze object prototypes or use Object.create(null) for untrusted keys. 2) SQL/NoSQL Injection: use parameterized queries (ORM/ODM) and sanitize inputs. 3) XSS: escape HTML output and use Helmet middleware for secure HTTP headers. 4) Dependency vulnerabilities: regularly run npm audit or use Snyk/Dependabot.",
         "// 1. helmet for security headers\nconst helmet = require('helmet');\napp.use(helmet());\n\n// 2. Safe objects (prevents prototype pollution)\nconst obj = Object.create(null);\n\n// 3. Parameterized query (prevents SQLi)\ndb.query('SELECT * FROM users WHERE id = $1', [userId]);",
         "Regularly audit production dependencies using npm audit or yarn audit to patch CVEs."),
    ],

    # =====================================================================
    "Phase 4: MongoDB & PostgreSQL": [
        ("BASIC", 5, "When should you use MongoDB vs PostgreSQL?",
         "MongoDB: flexible documents, nested/hierarchical data, rapidly changing schemas, horizontal scaling. PostgreSQL: relational data, complex joins, ACID transactions, strong consistency. Rule: if data has relationships and needs integrity → PostgreSQL. If schema is fluid and data is nested → MongoDB.",
         "// MongoDB — flexible nested document\n{\n  _id: '123',\n  name: 'Nazmul',\n  addresses: [\n    { type: 'home', city: 'Dhaka' },\n    { type: 'work', city: 'Mirpur' }\n  ]\n}\n\n// PostgreSQL — normalized\n-- users: id, name\n-- addresses: id, user_id FK, type, city",
         "Need ACID transactions and complex joins? PostgreSQL. Need schema flexibility and scale? MongoDB."),

        ("BASIC", 5, "What are database indexes and why do they matter?",
         "Indexes are like a book's index — instead of reading every page (full table scan), you jump directly to the right page. Without an index: O(n) scan. With an index (B-tree): O(log n). Trade-off: indexes speed reads but slow writes and use storage. Index columns you query often.",
         "-- PostgreSQL\nCREATE INDEX idx_users_email ON users(email);\nCREATE INDEX idx_posts_user_created\n  ON posts(user_id, created_at DESC); -- composite\n\n-- MongoDB\ndb.users.createIndex({ email: 1 }, { unique: true });\ndb.orders.createIndex(\n  { userId: 1, createdAt: -1 }\n);",
         "Use EXPLAIN ANALYZE (Postgres) or .explain('executionStats') (MongoDB) to verify index usage."),

        ("BASIC", 5, "What is database normalization?",
         "Normalization organizes data to reduce redundancy and improve integrity. 1NF: no repeating groups (each cell has one value). 2NF: 1NF + no partial dependencies. 3NF: 2NF + no transitive dependencies. In practice, normalize first, then selectively denormalize for read performance.",
         "-- UNNORMALIZED (bad)\n-- orders: id, customer_name, customer_email, product, price\n\n-- NORMALIZED (3NF)\n-- customers: id, name, email\n-- products: id, name, price\n-- orders: id, customer_id FK, product_id FK, quantity\n\n-- Denormalization (for read perf)\n-- order_summaries: id, customer_name, total\n-- Materialized view or cache",
         "Normalize for writes (data integrity), denormalize for reads (query speed). Balance both."),

        ("INTERMEDIATE", 5, "What is the N+1 query problem and how do you solve it?",
         "N+1 occurs when you fetch N records then make 1 extra query per record to get related data. 100 posts + 1 author query each = 101 queries. Fix: SQL JOINs, ORM eager loading (include/populate), or DataLoader batching in GraphQL.",
         "// N+1 problem\nconst posts = await Post.findAll(); // 1 query\nfor (const post of posts) {\n  // N queries!\n  const author = await User.findById(post.userId);\n}\n\n// Fix: eager load (1 JOIN query)\nconst posts = await Post.findAll({\n  include: [{ model: User, as: 'author' }]\n});\n\n// MongoDB fix: $lookup\ndb.posts.aggregate([\n  { $lookup: {\n    from: 'users', localField: 'userId',\n    foreignField: '_id', as: 'author'\n  }}\n]);",
         "Enable query logging in development to detect N+1 — Mongoose debug mode, Sequelize logging: true."),

        ("INTERMEDIATE", 4, "Explain MongoDB's aggregation pipeline.",
         "The aggregation pipeline processes documents through sequential stages, each transforming the output for the next. Think of it as a Unix pipe: data flows through stages. Key stages: $match (filter), $group (aggregate), $project (reshape), $sort, $lookup (join), $unwind (flatten arrays).",
         "db.orders.aggregate([\n  { $match: { status: 'completed' } },\n  { $group: {\n    _id: '$userId',\n    totalSpent: { $sum: '$amount' },\n    orderCount: { $sum: 1 }\n  }},\n  { $lookup: {\n    from: 'users',\n    localField: '_id',\n    foreignField: '_id',\n    as: 'user'\n  }},\n  { $unwind: '$user' },\n  { $sort: { totalSpent: -1 } },\n  { $limit: 10 }\n]);",
         "Always put $match as early as possible in the pipeline to reduce document count in later stages."),

        ("INTERMEDIATE", 4, "What are PostgreSQL transactions and ACID properties?",
         "ACID — the 4 guarantees of reliable transactions: Atomicity (all or nothing), Consistency (valid state before/after), Isolation (concurrent transactions don't interfere), Durability (committed data survives crashes). If any operation fails, everything rolls back.",
         "BEGIN;\n\nUPDATE accounts\n  SET balance = balance - 500\n  WHERE id = 1;\n\nUPDATE accounts\n  SET balance = balance + 500\n  WHERE id = 2;\n\nCOMMIT; -- Both succeed or both roll back\n\n-- Savepoints for partial rollback\nSAVEPOINT before_step;\n-- ... more operations ...\nROLLBACK TO SAVEPOINT before_step;",
         "MongoDB 4.0+ supports multi-document ACID transactions, but they add overhead vs SQL."),

        ("INTERMEDIATE", 4, "Compare Prisma vs Drizzle ORM.",
         "Prisma: declarative schema (schema.prisma), auto-generated type-safe client, great DX, migrations built-in, slightly heavier. Drizzle: SQL-like syntax in TypeScript, lighter weight, closer to raw SQL, better for edge/serverless. Prisma for productivity, Drizzle for control and performance.",
         "// Prisma — declarative\nconst user = await prisma.user.findUnique({\n  where: { email: 'test@test.com' },\n  include: { posts: true },\n});\n\n// Drizzle — SQL-like\nconst user = await db\n  .select()\n  .from(users)\n  .where(eq(users.email, 'test@test.com'))\n  .leftJoin(posts, eq(users.id, posts.userId));",
         "Prisma for rapid development. Drizzle for serverless/edge where cold start matters."),

        ("INTERMEDIATE", 4, "Explain PostgreSQL JSON/JSONB columns.",
         "PostgreSQL can store JSON data in columns — JSONB is the binary format (faster queries, indexable). This gives you document-like flexibility within a relational database. You can query, index, and validate JSON fields. Best of both worlds: relational + flexible.",
         "-- Create with JSONB\nCREATE TABLE products (\n  id SERIAL PRIMARY KEY,\n  name TEXT NOT NULL,\n  attributes JSONB DEFAULT '{}'\n);\n\n-- Insert\nINSERT INTO products (name, attributes)\nVALUES ('Laptop', '{\"ram\": 16, \"color\": \"silver\"}');\n\n-- Query JSONB\nSELECT * FROM products\nWHERE attributes->>'color' = 'silver';\n\n-- GIN index for JSONB\nCREATE INDEX idx_prod_attrs ON products\n  USING GIN (attributes);",
         "Use JSONB (not JSON) — it's parsed on write, faster on read, and supports indexing."),

        ("INTERMEDIATE", 4, "How do you handle database migrations?",
         "Migrations are version-controlled schema changes — each migration file describes a forward change (up) and a rollback (down). They ensure every environment has the same schema. Never modify production schema manually — always use migrations.",
         "// Prisma migration\n// prisma/migrations/001_add_posts/migration.sql\nCREATE TABLE posts (\n  id SERIAL PRIMARY KEY,\n  title TEXT NOT NULL,\n  content TEXT,\n  author_id INT REFERENCES users(id),\n  created_at TIMESTAMP DEFAULT NOW()\n);\n\n// CLI commands\n// npx prisma migrate dev --name add_posts\n// npx prisma migrate deploy  (production)\n// npx prisma migrate reset    (dev only)\n\n// Knex.js migration\nexports.up = (knex) => knex.schema.createTable('posts', t => {\n  t.increments('id');\n  t.string('title').notNullable();\n});",
         "Always test migrations on a staging database before running in production."),

        ("INTERMEDIATE", 3, "Explain MongoDB schema design: embedding vs referencing.",
         "Embed when: data is always accessed together, bounded one-to-few, rarely changes independently. Reference when: many-to-many, accessed independently, unbounded growth, or documents risk exceeding 16MB. Remember: embed for reads, reference for writes.",
         "// Embed — post with few comments\n{\n  _id: 'post1',\n  title: 'Hello World',\n  comments: [\n    { author: 'Ali', text: 'Great!' }\n  ]\n}\n\n// Reference — user with millions of orders\n// users: { _id, name, email }\n// orders: { _id, userId: ObjectId, amount }\n\n// Query with $lookup\ndb.orders.aggregate([\n  { $lookup: {\n    from: 'users',\n    localField: 'userId',\n    foreignField: '_id',\n    as: 'user'\n  }}\n]);",
         "MongoDB documents have a hard 16MB limit — never embed unbounded arrays."),

        ("INTERMEDIATE", 3, "What is full-text search and how do databases support it?",
         "Full-text search finds documents by words/phrases with relevance ranking — unlike LIKE which does pattern matching. PostgreSQL has built-in tsvector/tsquery. MongoDB has text indexes. For advanced needs (fuzzy, faceted, autocomplete), use Elasticsearch.",
         "-- PostgreSQL full-text search\nALTER TABLE articles ADD COLUMN search_vector tsvector;\nUPDATE articles SET search_vector =\n  to_tsvector('english', title || ' ' || body);\nCREATE INDEX idx_search ON articles USING GIN(search_vector);\n\nSELECT title, ts_rank(search_vector, query) AS rank\nFROM articles, to_tsquery('react & hooks') query\nWHERE search_vector @@ query\nORDER BY rank DESC;\n\n// MongoDB text search\ndb.articles.createIndex({ title: 'text', body: 'text' });\ndb.articles.find({ $text: { $search: 'react hooks' } });",
         "PostgreSQL full-text search is surprisingly powerful — try it before adding Elasticsearch."),

        ("INTERMEDIATE", 3, "Explain MongoDB change streams.",
         "Change streams let you watch a collection for real-time changes (insert, update, delete) — like database triggers but application-level. Built on the oplog. Perfect for real-time sync, cache invalidation, and event-driven architectures.",
         "const pipeline = [\n  { $match: { operationType: { $in: ['insert', 'update'] } } },\n  { $match: { 'fullDocument.status': 'published' } }\n];\n\nconst changeStream = db.collection('posts').watch(pipeline);\n\nchangeStream.on('change', (change) => {\n  switch (change.operationType) {\n    case 'insert':\n      notifySubscribers(change.fullDocument);\n      break;\n    case 'update':\n      invalidateCache(change.documentKey._id);\n      break;\n  }\n});",
         "Change streams require a replica set — they won't work on standalone MongoDB instances."),

        ("ADVANCED", 4, "Explain read replicas and database sharding.",
         "Read Replicas: copies of the primary DB that handle read traffic. Writes go to primary, reads go to replicas — reduces read pressure. Sharding: partitions data across multiple databases by shard key. Each shard holds a subset. Together they enable massive horizontal scaling.",
         "// Read/write separation\nawait primaryPool.query('INSERT INTO orders...');\nawait replicaPool.query('SELECT * FROM orders WHERE userId = $1', [id]);\n\n// MongoDB sharding\nsh.enableSharding('mydb');\nsh.shardCollection('mydb.users', { region: 'hashed' });\n// Asia users -> Shard A\n// Europe users -> Shard B\n// Queries route automatically",
         "Choose shard keys carefully — a bad key causes hot spots where one shard gets all the traffic."),

        ("ADVANCED", 4, "How do you optimize a slow SQL query?",
         "7-step optimization: 1) EXPLAIN ANALYZE — see the query plan. 2) Check for missing indexes. 3) Avoid SELECT * — only fetch needed columns. 4) Don't wrap indexed columns in functions. 5) Paginate large results. 6) Use covering indexes. 7) Cache hot queries in Redis.",
         "-- Slow: function prevents index use\nSELECT * FROM users\nWHERE LOWER(email) = 'test@example.com';\n\n-- Fix: index on expression\nCREATE INDEX idx_lower_email\n  ON users(LOWER(email));\n\n-- Better projection\nSELECT id, name, email FROM users\nWHERE LOWER(email) = 'test@example.com';\n\n-- Check plan\nEXPLAIN ANALYZE\nSELECT id, name FROM users\nWHERE email = 'x@y.com';",
         "'Seq Scan' in EXPLAIN output = no index used. 'Index Scan' = good. 'Bitmap Heap Scan' = ok."),

        ("ADVANCED", 3, "Explain database connection pooling.",
         "Creating a new DB connection is expensive (TCP handshake, auth, SSL, memory allocation). Connection pooling maintains a pool of pre-established connections reused across requests. Without pooling, high traffic exhausts DB connections and crashes the database.",
         "// PostgreSQL with pg pool\nconst { Pool } = require('pg');\n\nconst pool = new Pool({\n  host: process.env.DB_HOST,\n  database: process.env.DB_NAME,\n  user: process.env.DB_USER,\n  password: process.env.DB_PASS,\n  max: 20,          // max connections\n  idleTimeoutMillis: 30000,\n  connectionTimeoutMillis: 2000,\n});\n\n// Reuses existing connection from pool\nconst result = await pool.query(\n  'SELECT * FROM users WHERE id = $1', [id]\n);",
         "Tune max pool size based on DB max_connections. Rule: pool size = (number of cores * 2) + effective spindle count."),

        ("ADVANCED", 3, "What are PostgreSQL Common Table Expressions (CTEs)?",
         "CTEs (WITH clauses) are named temporary result sets within a query. They make complex queries readable by breaking them into logical steps. Recursive CTEs handle tree/hierarchical data (org charts, category trees). Think of CTEs as 'query variables'.",
         "-- Regular CTE\nWITH active_users AS (\n  SELECT id, name FROM users WHERE active = true\n),\nuser_orders AS (\n  SELECT user_id, SUM(amount) as total\n  FROM orders GROUP BY user_id\n)\nSELECT u.name, COALESCE(o.total, 0) as total\nFROM active_users u\nLEFT JOIN user_orders o ON u.id = o.user_id;\n\n-- Recursive CTE (org chart)\nWITH RECURSIVE org AS (\n  SELECT id, name, manager_id, 0 as depth\n  FROM employees WHERE manager_id IS NULL\n  UNION ALL\n  SELECT e.id, e.name, e.manager_id, o.depth + 1\n  FROM employees e JOIN org o ON e.manager_id = o.id\n)\nSELECT * FROM org;",
         "Recursive CTEs replace what would be loops in application code — let the database handle it."),

        ("ADVANCED", 3, "How do you handle database backup and disaster recovery?",
         "Three strategies: 1) Logical backups (pg_dump/mongodump) — portable but slow for large DBs. 2) Physical backups (file system snapshots, pg_basebackup) — fast but DB-specific. 3) Point-in-time recovery (WAL archiving / oplog) — restore to any moment. Test restores regularly!",
         "# PostgreSQL backup\npg_dump -Fc mydb > backup.dump\npg_restore -d mydb backup.dump\n\n# Automated with cron\n0 2 * * * pg_dump -Fc mydb > /backups/mydb_$(date +%Y%m%d).dump\n\n# MongoDB backup\nmongodump --uri='mongodb://...' --out=/backups/$(date +%Y%m%d)\nmongorestore --uri='mongodb://...' /backups/20250101\n\n# Point-in-time recovery (PostgreSQL WAL)\narchive_mode = on\narchive_command = 'cp %p /wal_archive/%f'",
         "An untested backup is not a backup. Regularly practice restoring from backups."),

        ("ADVANCED", 4, "Explain database locking mechanisms (Shared, Exclusive, Optimistic, Pessimistic).",
         "Locks prevent race conditions. Shared lock (S) allows multiple reads but blocks writes. Exclusive lock (X) blocks both reads and writes. Pessimistic locking locks rows when reading (SELECT ... FOR UPDATE) until transaction completes. Optimistic locking uses a version column and checks if it has changed at update time, retrying on conflict.",
         "-- Pessimistic lock (blocks until current transaction completes)\nBEGIN;\nSELECT * FROM inventory WHERE item_id = 1 FOR UPDATE;\nUPDATE inventory SET stock = stock - 1 WHERE item_id = 1;\nCOMMIT;\n\n-- Optimistic lock (no database-level locking)\nUPDATE inventory SET stock = stock - 1, version = version + 1\nWHERE item_id = 1 AND version = 5; -- fails if version changed!",
         "Pessimistic locking is better for high-contention, write-heavy rows. Optimistic locking is better for read-heavy rows."),

        ("INTERMEDIATE", 4, "Explain the CAP Theorem and how it applies to MongoDB and PostgreSQL.",
         "The CAP Theorem states a distributed system can guarantee at most two of: Consistency, Availability, Partition tolerance. PostgreSQL is traditionally a CA system (prioritizes ACID consistency/availability, though partitions cause issues). MongoDB is a CP system (Consistency + Partition tolerance) by default: if a network partition isolates the primary node, secondaries refuse writes while electing a new primary.",
         "// MongoDB CP setting: replica sets elect new primary.\n// During elections, writes are blocked (losing Availability).\n// Read preference can be tuned to read stale data (prioritizing Availability):\nconst cursor = db.collection('posts').find({}).readPref('secondary');",
         "No system is 100% Consistent and 100% Available during a network partition (P) — you must choose C or A."),

        ("ADVANCED", 4, "Explain PostgreSQL Window Functions with examples.",
         "Window functions perform calculations across a set of table rows related to the current row without grouping them into a single output row. They keep individual row identities intact. Syntax uses the OVER clause, often combined with PARTITION BY and ORDER BY. Common functions include ROW_NUMBER(), RANK(), and DENSE_RANK().",
         "-- Get top 3 salary earners per department\nWITH ranked_salaries AS (\n  SELECT name, department, salary,\n         DENSE_RANK() OVER (\n           PARTITION BY department\n           ORDER BY salary DESC\n         ) as rank\n  FROM employees\n)\nSELECT * FROM ranked_salaries WHERE rank <= 3;",
         "Window functions are powerful for analytical queries, reporting, and ranking without complex self-joins."),

        ("INTERMEDIATE", 3, "How do you handle soft deletes and what are the index/query implications?",
         "Soft deleting marks a record as deleted (e.g. is_deleted = true or deleted_at = TIMESTAMP) rather than removing it. Query implication: every query must filter with WHERE deleted_at IS NULL. Index implication: you should create partial/filtered indexes on active records to avoid scanning deleted rows, especially if deletes are frequent.",
         "-- 1. Create table with soft delete column\nALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;\n\n-- 2. Create partial index for active users only\nCREATE INDEX idx_active_users_email ON users(email) WHERE deleted_at IS NULL;\n\n-- 3. Querying active users\nSELECT * FROM users WHERE email = 'test@test.com' AND deleted_at IS NULL;",
         "Partial indexes keep indexes small and queries fast by ignoring soft-deleted rows entirely."),

        ("ADVANCED", 4, "Explain Database Sharding vs Partitioning.",
         "Partitioning (vertical or horizontal) splits tables within a single database instance (e.g., PostgreSQL table partitioning by date range). Sharding splits data across multiple independent database instances or servers (shared-nothing architecture). Partitioning simplifies queries on large tables on a single server, while sharding scales writes and storage across multiple hardware nodes.",
         "-- PostgreSQL declarative range partitioning (Horizontal Partitioning)\nCREATE TABLE orders (\n  id SERIAL,\n  order_date DATE NOT NULL,\n  amount DECIMAL\n) PARTITION BY RANGE (order_date);\n\n-- Create sub-tables\nCREATE TABLE orders_2025 PARTITION OF orders\n  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');",
         "Partition first to handle large tables. Shard only when a single database server cannot handle the throughput."),
    ],

    "Phase 5: System Design & DSA": [
        ("BASIC", 5, "What is Big O notation? Give examples.",
         "Big O describes how an algorithm scales with input size — it's the worst-case growth rate. O(1) constant (hash lookup), O(log n) binary search, O(n) linear scan, O(n log n) merge sort, O(n²) nested loops, O(2^n) recursive subsets. Always state both time AND space complexity.",
         "// O(1) — hash lookup\nconst map = new Map();\nmap.get('key'); // constant\n\n// O(n) — linear scan\narray.find(x => x === target);\n\n// O(log n) — binary search\nfunction binarySearch(arr, target) {\n  let lo = 0, hi = arr.length - 1;\n  while (lo <= hi) {\n    const mid = (lo + hi) >> 1;\n    if (arr[mid] === target) return mid;\n    arr[mid] < target ? lo = mid+1 : hi = mid-1;\n  }\n  return -1;\n}",
         "In interviews: state time complexity, then space complexity — both matter."),

        ("BASIC", 5, "Two Sum problem — optimal approach.",
         "Naive: O(n²) nested loops. Optimal: one pass with a hash map — O(n) time, O(n) space. For each number, check if its complement (target - num) exists in the map. This 'complement lookup' pattern solves dozens of interview problems.",
         "function twoSum(nums, target) {\n  const map = new Map(); // value -> index\n\n  for (let i = 0; i < nums.length; i++) {\n    const complement = target - nums[i];\n\n    if (map.has(complement)) {\n      return [map.get(complement), i];\n    }\n    map.set(nums[i], i);\n  }\n  return [];\n}\n\n// twoSum([2,7,11,15], 9) -> [0,1]\n// O(n) time, O(n) space",
         "The complement pattern in a hash map is the most common interview optimization technique."),

        ("BASIC", 5, "Reverse a linked list.",
         "Use three pointers: prev, current, next. At each step: save next, point current backward to prev, advance prev and current. After the loop, prev is the new head. This is the most frequently asked data structure question.",
         "function reverseList(head) {\n  let prev = null;\n  let current = head;\n\n  while (current) {\n    const next = current.next; // save\n    current.next = prev;       // reverse\n    prev = current;            // advance\n    current = next;\n  }\n  return prev; // new head\n}\n\n// 1->2->3->null becomes 3->2->1->null\n// O(n) time, O(1) space",
         "Memorize the 3-pointer technique: save, reverse, advance. Works for many linked list problems."),

        ("BASIC", 5, "Valid Parentheses — stack solution.",
         "Use a stack. For each character: if opening bracket, push its expected closing bracket. If closing bracket, pop from stack and compare. If mismatch or stack not empty at end, invalid. This is the classic stack problem — demonstrates LIFO perfectly.",
         "function isValid(s) {\n  const stack = [];\n  const map = { '(': ')', '[': ']', '{': '}' };\n\n  for (const char of s) {\n    if (map[char]) {\n      stack.push(map[char]); // push expected closer\n    } else {\n      if (stack.pop() !== char) return false;\n    }\n  }\n  return stack.length === 0;\n}\n\n// isValid('([{}])') -> true\n// isValid('([)]')   -> false\n// O(n) time, O(n) space",
         "Push the EXPECTED closing bracket — this avoids complex if/else when comparing."),

        ("INTERMEDIATE", 5, "What is the difference between vertical and horizontal scaling?",
         "Vertical: add more CPU/RAM to one machine. Simple but has a ceiling and is a single point of failure. Horizontal: add more machines behind a load balancer. No ceiling, no SPOF, but requires stateless design. Modern systems prefer horizontal for reliability.",
         "// Horizontal scaling requires stateless services\n// Bad: session in memory (only one server has it)\napp.use(session({ secret: 'x', resave: false }));\n\n// Good: session in Redis (shared across servers)\napp.use(session({\n  store: new RedisStore({ client: redisClient }),\n  secret: process.env.SESSION_SECRET,\n  resave: false,\n}));\n\n// JWT is inherently stateless — even better",
         "Horizontal scaling + stateless design is the foundation of cloud-native architecture."),

        ("INTERMEDIATE", 5, "Explain caching strategies: cache-aside, write-through, write-behind.",
         "Cache-aside (lazy loading): check cache → miss → load from DB → populate cache. Most common. Write-through: write to cache AND DB simultaneously — consistent but slower writes. Write-behind: write to cache first, async persist to DB — fastest writes, risk of data loss on crash.",
         "// Cache-aside pattern\nasync function getUser(id) {\n  const key = 'user:' + id;\n  const cached = await redis.get(key);\n  if (cached) return JSON.parse(cached);\n\n  const user = await db.findById(id);\n  await redis.setex(key, 3600, JSON.stringify(user));\n  return user;\n}\n\n// Invalidate on update\nasync function updateUser(id, data) {\n  await db.update(id, data);\n  await redis.del('user:' + id);\n}",
         "Always set TTL on cached entries — never cache without expiry."),

        ("INTERMEDIATE", 4, "Design a URL shortener system.",
         "Requirements: shorten URLs, redirect fast, 1M+ requests/day. Components: API server, ID generator (base62 of auto-increment or hash), Redis (fast lookup), PostgreSQL (persistent store), CDN for edge redirect. Keep it simple — generate short code, store mapping, redirect on hit.",
         "// ID generation (base62)\nconst CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';\nfunction encode(num) {\n  let result = '';\n  while (num > 0) {\n    result = CHARS[num % 62] + result;\n    num = Math.floor(num / 62);\n  }\n  return result.padStart(7, '0');\n}\n\n// Request flow:\n// POST /shorten -> generate ID -> store in DB + Redis\n// GET /:id -> Redis lookup (cache hit ~99%)\n//          -> 301 redirect to original URL",
         "Always start system design: requirements → estimation → high-level → deep dive."),

        ("INTERMEDIATE", 4, "Design a real-time chat system.",
         "Components: WebSocket server (persistent connections), Redis Pub/Sub (cross-server messaging), message storage (DB), presence tracking (online/offline). Users connect via WebSocket, messages are broadcast through Redis pub/sub to all servers, then persisted to DB asynchronously.",
         "// Architecture:\n// Client <-> WebSocket Server <-> Redis Pub/Sub\n//                                    |\n//                              Message Queue\n//                                    |\n//                               MongoDB/Postgres\n\n// Key decisions:\n// 1. WebSocket for real-time delivery\n// 2. Redis pub/sub for cross-server broadcast\n// 3. Message queue for async persistence\n// 4. Online status: Redis SET with TTL\n// 5. Message history: cursor-based pagination\n// 6. Read receipts: separate events",
         "For 1:1 chats, route through user channels. For group chats, use room-based pub/sub."),

        ("INTERMEDIATE", 4, "Explain BFS vs DFS traversal.",
         "BFS (Breadth-First Search): explores level by level using a queue. Best for shortest path in unweighted graphs. DFS (Depth-First Search): goes deep before backtracking using a stack/recursion. Best for exhaustive search, cycle detection, topological sort.",
         "// BFS — level by level (queue)\nfunction bfs(root) {\n  const queue = [root];\n  while (queue.length) {\n    const node = queue.shift();\n    console.log(node.val);\n    if (node.left) queue.push(node.left);\n    if (node.right) queue.push(node.right);\n  }\n}\n\n// DFS — go deep (recursion/stack)\nfunction dfs(node) {\n  if (!node) return;\n  console.log(node.val); // pre-order\n  dfs(node.left);\n  dfs(node.right);\n}",
         "BFS = queue = level-by-level. DFS = stack/recursion = branch-by-branch."),

        ("INTERMEDIATE", 4, "Explain the sliding window technique.",
         "Sliding window maintains a 'window' of elements as you traverse an array — expand the right side to include, shrink the left side to exclude. It turns O(n²) brute force into O(n). Used for: max sum subarray, longest substring without repeats, minimum window containing all characters.",
         "// Max sum subarray of size k\nfunction maxSubarraySum(arr, k) {\n  let windowSum = 0;\n  for (let i = 0; i < k; i++) windowSum += arr[i];\n\n  let maxSum = windowSum;\n  for (let i = k; i < arr.length; i++) {\n    windowSum += arr[i] - arr[i - k]; // slide\n    maxSum = Math.max(maxSum, windowSum);\n  }\n  return maxSum;\n}\n\n// Longest substring without repeating chars\nfunction lengthOfLongest(s) {\n  const seen = new Map();\n  let left = 0, max = 0;\n  for (let right = 0; right < s.length; right++) {\n    if (seen.has(s[right]))\n      left = Math.max(left, seen.get(s[right]) + 1);\n    seen.set(s[right], right);\n    max = Math.max(max, right - left + 1);\n  }\n  return max;\n}",
         "When you see 'subarray' or 'substring' in a problem, think sliding window first."),

        ("INTERMEDIATE", 4, "What is the circuit breaker pattern?",
         "Circuit breaker prevents cascading failures when a service is down. Three states: Closed (normal, requests pass through), Open (service is down, requests fail immediately — no waiting), Half-Open (test with a few requests to see if service recovered). Like an electrical circuit breaker — stops the damage.",
         "class CircuitBreaker {\n  constructor(fn, { threshold = 5, timeout = 30000 } = {}) {\n    this.fn = fn;\n    this.failures = 0;\n    this.threshold = threshold;\n    this.timeout = timeout;\n    this.state = 'CLOSED';\n    this.nextAttempt = 0;\n  }\n\n  async call(...args) {\n    if (this.state === 'OPEN') {\n      if (Date.now() < this.nextAttempt)\n        throw new Error('Circuit is OPEN');\n      this.state = 'HALF_OPEN';\n    }\n    try {\n      const result = await this.fn(...args);\n      this.reset();\n      return result;\n    } catch (err) {\n      this.recordFailure();\n      throw err;\n    }\n  }\n}",
         "Use circuit breakers around all external service calls — databases, APIs, third-party services."),

        ("INTERMEDIATE", 3, "Merge two sorted arrays.",
         "Use two pointers, one for each array. Compare elements at both pointers, push the smaller one, advance that pointer. When one array is exhausted, append the remainder of the other. This is the merge step of merge sort. O(n + m) time, O(n + m) space.",
         "function mergeSorted(a, b) {\n  const result = [];\n  let i = 0, j = 0;\n\n  while (i < a.length && j < b.length) {\n    if (a[i] <= b[j]) result.push(a[i++]);\n    else result.push(b[j++]);\n  }\n\n  // Append remaining\n  while (i < a.length) result.push(a[i++]);\n  while (j < b.length) result.push(b[j++]);\n\n  return result;\n}\n\n// mergeSorted([1,3,5], [2,4,6]) -> [1,2,3,4,5,6]",
         "Two-pointer on sorted data is a fundamental technique — appears in many interview problems."),

        ("INTERMEDIATE", 3, "Explain event-driven architecture.",
         "Instead of synchronous request-response, services communicate by emitting and consuming events. Event producers don't know or care about consumers. This enables loose coupling, scalability, and resilience. Events are stored in brokers (Kafka, RabbitMQ) for reliable delivery.",
         "// Event-driven flow\n// OrderService emits 'OrderPlaced'\n// ↓ (async via message broker)\n// PaymentService listens → processes payment\n// InventoryService listens → reserves stock\n// NotificationService listens → sends email\n\n// Benefits:\n// 1. Services are independent\n// 2. Adding consumers doesn't change producer\n// 3. Events can be replayed\n// 4. Natural audit trail\n\n// Kafka example:\nawait producer.send({\n  topic: 'orders',\n  messages: [{ value: JSON.stringify(order) }]\n});",
         "Event sourcing stores events as the source of truth — you can rebuild state by replaying events."),

        ("ADVANCED", 4, "How would you design a real-time notification system?",
         "Components: event producers (any service), message broker (Kafka), notification service (routes to channels), delivery channels (WebSocket for online, push/email/SMS for offline). Use fan-out pattern for broadcasting. Store preferences so users control what they receive.",
         "// Producer emits event\nawait kafka.send({\n  topic: 'notifications',\n  messages: [{ value: JSON.stringify({\n    type: 'ORDER_PLACED',\n    userId: user.id,\n    orderId: order.id\n  })}]\n});\n\n// Consumer routes notifications\nkafka.on('message', async msg => {\n  const event = JSON.parse(msg.value);\n  // WebSocket for online users\n  io.to('user:' + event.userId).emit('notification', {\n    type: event.type, message: 'Order confirmed!'\n  });\n  // Email for offline users\n  if (!onlineUsers.has(event.userId))\n    await emailQueue.add(event);\n});",
         "Separate notification routing from delivery — use dedicated workers per channel."),

        ("ADVANCED", 4, "Explain the CAP theorem.",
         "CAP: a distributed system can guarantee only 2 of 3 — Consistency (all nodes see same data), Availability (every request gets a response), Partition Tolerance (works despite network failures). Since network partitions are inevitable, the real choice is CP (consistent but might refuse requests) or AP (available but might serve stale data).",
         "// CP systems: MongoDB, ZooKeeper, HBase\n// During partition: refuse writes to stay consistent\n// Use when: bank balances, inventory counts\n\n// AP systems: Cassandra, DynamoDB, CouchDB\n// During partition: serve potentially stale data\n// Use when: social feeds, product catalog\n\n// Tunable consistency example (Cassandra):\nCONSISTENCY QUORUM; -- majority of nodes must agree\nCONSISTENCY EVENTUAL; -- fast, may read stale",
         "Modern systems often have configurable consistency (e.g., MongoDB readConcern/writeConcern)."),

        ("ADVANCED", 4, "Explain database connection pooling.",
         "Creating a new DB connection is expensive (TCP handshake, auth, memory). Connection pooling maintains a pool of pre-established connections reused across requests. Without pooling, high traffic exhausts DB connections. pg-pool (Postgres), Mongoose (MongoDB) pool by default.",
         "// PostgreSQL with pg pool\nconst { Pool } = require('pg');\n\nconst pool = new Pool({\n  host: process.env.DB_HOST,\n  database: process.env.DB_NAME,\n  user: process.env.DB_USER,\n  password: process.env.DB_PASS,\n  max: 20,          // max connections\n  idleTimeoutMillis: 30000,\n  connectionTimeoutMillis: 2000,\n});\n\n// Reuses existing connection from pool\nconst result = await pool.query(\n  'SELECT * FROM users WHERE id = $1', [id]\n);",
         "Tune max pool size based on DB max_connections. Rule: pool size = (number of cores * 2) + effective spindle count."),

        ("ADVANCED", 3, "Design an API gateway.",
         "API gateway is the single entry point for all client requests. It handles: routing to microservices, authentication, rate limiting, request/response transformation, caching, logging, and load balancing. Clients talk to one gateway instead of many services.",
         "// API Gateway responsibilities:\n// 1. Route: /api/users/* -> user-service\n// 2. Route: /api/orders/* -> order-service\n// 3. Auth: verify JWT before forwarding\n// 4. Rate limit: per user/IP\n// 5. Transform: aggregate responses\n// 6. Cache: store frequent reads\n// 7. Circuit break: fallback on failure\n\n// Tools: Kong, AWS API Gateway,\n//        Express gateway, Nginx\n\n// Simple Express gateway\napp.use('/api/users', authMiddleware,\n  proxy('http://user-service:3001'));\napp.use('/api/orders', authMiddleware,\n  proxy('http://order-service:3002'));",
         "Keep the gateway thin — business logic belongs in services, not the gateway."),

        ("ADVANCED", 3, "Explain hash table collision resolution.",
         "When two keys hash to the same slot, you have a collision. Two strategies: Chaining (each slot holds a linked list of entries) — simple, grows naturally. Open Addressing (probe for next empty slot: linear, quadratic, double hashing) — better cache performance, fixed size.",
         "// Chaining: slot holds a list\n// Hash table:\n// [0] -> null\n// [1] -> ('alice', 25) -> ('bob', 30)\n// [2] -> ('charlie', 22)\n\n// Simple hash map with chaining\nclass HashMap {\n  constructor(size = 53) {\n    this.table = new Array(size);\n  }\n  hash(key) {\n    let total = 0;\n    for (let i = 0; i < key.length; i++)\n      total = (total * 31 + key.charCodeAt(i)) % this.table.length;\n    return total;\n  }\n  set(key, val) {\n    const idx = this.hash(key);\n    if (!this.table[idx]) this.table[idx] = [];\n    this.table[idx].push([key, val]);\n  }\n}",
         "JavaScript Map uses hash tables internally — O(1) average for get/set/delete."),

        ("ADVANCED", 4, "How do you design a distributed Rate Limiter?",
         "Four common algorithms: 1) Token Bucket: bucket holds max tokens, refilled at a rate. Allows bursts. 2) Leaky Bucket: queue processed at a constant rate. Smooths traffic. 3) Sliding Window Log: store timestamps of requests in Redis ZSET. 4) Sliding Window Counter: compute rate combining current and previous window counts (low memory).",
         "// Sliding Window Counter conceptual implementation in Redis\nasync function isRateLimited(userId, limit, windowSizeSecs) {\n  const now = Date.now();\n  const clearBefore = now - (windowSizeSecs * 1000);\n  const key = `rate:${userId}`;\n  const tx = redis.multi();\n  tx.zremrangebyscore(key, 0, clearBefore);\n  tx.zcard(key);\n  tx.zadd(key, now, now.toString());\n  tx.expire(key, windowSizeSecs);\n  const results = await tx.exec();\n  return results[1][1] >= limit;\n}",
         "Use Redis for distributed rate limiting to share the state across multiple application servers."),

        ("ADVANCED", 3, "Design a Content Delivery Network (CDN) and explain how edge caching works.",
         "A CDN is a distributed network of proxy servers deployed globally. Routing (Anycast or GeoDNS) directs clients to the closest edge server. Edge caching stores files locally. If a cache miss occurs, the edge fetches from the origin, caches it, and returns it. Uses HTTP caching headers like Cache-Control.",
         "// Caching headers sent by origin:\n// Cache-Control: public, max-age=31536000, s-maxage=86400\n// - max-age: browser caches for 1 year\n// - s-maxage: CDN edge caches for 1 day\n\n// Purge endpoint to invalidate cache programmatically:\n// POST /api/v1/purge { files: ['/logo.png'] }\n// Purging is critical for immediate updates.",
         "CDNs are critical for lowering Time to First Byte (TTFB) and reducing load on origin servers."),

        ("ADVANCED", 4, "Explain the Consistent Hashing algorithm and its role in distributed systems.",
         "Traditional hashing (hash(key) % N) reshuffles almost all keys when N (number of servers) changes. Consistent Hashing maps servers and keys to a 360-degree circular ring. A key routes to the first server clockwise. Adding/removing a server only remaps 1/N of the keys. Virtual nodes (vnodes) distribute keys evenly.",
         "// Hash space: [0, 2^32 - 1]\n// Server A: hash = 100,000\n// Server B: hash = 2,000,000\n// Key X: hash = 500,000 -> Routes clockwise to Server B\n// If Server A goes offline, only keys on Server A remap to B.\n// Keys on Server B are unaffected.",
         "Consistent Hashing is used in DynamoDB, Cassandra, Memcached, and load balancers."),

        ("ADVANCED", 4, "Design a distributed unique ID generator (like Twitter Snowflake).",
         "Requirements: unique, time-sortable, 64-bit integer. Twitter Snowflake allocates: 1 bit (unused), 41 bits (timestamp in ms, 69 years lifetime), 10 bits (machine/datacenter ID, 1024 nodes), and 12 bits (sequence number, auto-incremented for IDs generated in the same ms, 4096 IDs/ms).",
         "// Layout: | 1-bit unused | 41-bit time | 10-bit node | 12-bit seq |\nconst EPOCH = 1600000000000n;\n\nfunction generateId(nodeId, seq) {\n  const timestamp = BigInt(Date.now()) - EPOCH;\n  return (timestamp << 22n) |\n         (BigInt(nodeId) << 12n) |\n         BigInt(seq);\n}",
         "Snowflake IDs are 64-bit sortable integers, which are highly index-friendly for databases."),

        ("INTERMEDIATE", 4, "Find the longest substring without repeating characters.",
         "Use the sliding window technique with two pointers (left and right) and a Map to track character indices. As right expands, if a character is repeated, move left to max(left, lastSeenIndex + 1) to exclude the repeat. This runs in O(n) time and O(min(a,b)) space.",
         "function longestUniqueSubstring(s) {\n  let maxLen = 0, left = 0;\n  const seen = new Map(); // char -> index\n  for (let right = 0; right < s.length; right++) {\n    const char = s[right];\n    if (seen.has(char)) {\n      left = Math.max(left, seen.get(char) + 1);\n    }\n    seen.set(char, right);\n    maxLen = Math.max(maxLen, right - left + 1);\n  }\n  return maxLen;\n}\n// longestUniqueSubstring('abcabcbb') -> 3",
         "Sliding window reduces what would be an O(n²) or O(n³) nested search to a clean O(n) linear pass."),

        ("ADVANCED", 3, "Design a File Upload system with multipart upload and resume capability.",
         "For large files, uploading in one request is fragile. Design: 1) Client initiates upload: server returns uploadId. 2) Client splits file into chunks (e.g. 5MB) and uploads them in parallel using presigned URLs with part numbers. 3) Server stores chunks in temp bucket. 4) Client completes upload: server merges chunks and verifies checksum.",
         "// 1. Initiate upload\n// POST /api/upload/initiate -> { uploadId: 'id', chunkUrls: [...] }\n\n// 2. Upload chunk in parallel\n// PUT /chunk-url-1?partNumber=1&uploadId=id -> ETag: 'etag1'\n\n// 3. Complete upload\n// POST /api/upload/complete -> { parts: [{ ETag: 'etag1', PartNumber: 1 }] }",
         "Multipart upload enables automatic retries of failed parts and parallel upload speedups."),

        ("ADVANCED", 4, "Explain LRU (Least Recently Used) Cache design and its implementation details.",
         "An LRU cache evicts the least recently accessed item when capacity is reached. Requirements: get and put operations must run in O(1) time. Implementation: use a Hash Map for O(1) key-to-node lookups, and a Doubly Linked List (DLL) to maintain access order. Accessed items move to the head, evictions happen at the tail.",
         "class Node {\n  constructor(key, val) {\n    this.key = key; this.val = val;\n    this.prev = null; this.next = null;\n  }\n}\n// HashMap contains references to DLL Nodes.\n// get(key): retrieve from map, move to DLL head, return value.\n// put(key, val): if exists, update + move to head. If new, add to head.\n//               if over capacity, delete DLL tail and remove from map.",
         "Using a DLL allows O(1) node removal and insertion, while a Map provides O(1) lookup."),
    ],

    # =====================================================================
    "Phase 6: Scalable Architecture & Production DevOps": [
        ("BASIC", 5, "What is the difference between monolithic and microservices architecture?",
         "Monolith: single deployable unit, all features in one codebase — simple to develop, test, and deploy. Microservices: independently deployable services, each owning its domain and database — enables independent scaling and team autonomy but adds operational complexity (networking, monitoring, debugging).",
         "// Monolith — one deployment\napp/\n  src/\n    auth/\n    users/\n    products/\n    payments/\n\n// Microservices — many deployments\nauth-service/     -> :3001\nuser-service/     -> :3002\nproduct-service/  -> :3003\npayment-service/  -> :3004\n// Each communicates via HTTP/gRPC/events\n// Each has its own database",
         "Most startups: start monolith, extract microservices when specific pain points appear."),

        ("BASIC", 5, "What is Docker and why is it used?",
         "Docker packages your app + all dependencies into a container — a portable unit that runs identically everywhere. 'Works on my machine' becomes 'works everywhere'. Containers share the host OS kernel (unlike VMs), start in seconds, and use minimal resources.",
         "# Multi-stage Dockerfile for Next.js\nFROM node:20-alpine AS deps\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\n\nFROM deps AS builder\nCOPY . .\nRUN npm run build\n\nFROM node:20-alpine AS runner\nWORKDIR /app\nCOPY --from=builder /app/.next ./.next\nCOPY --from=builder /app/public ./public\nCOPY --from=deps /app/node_modules ./node_modules\nEXPOSE 3000\nCMD [\"npm\", \"start\"]",
         "Multi-stage builds keep images small by excluding build tools from the final image."),

        ("BASIC", 5, "What is CI/CD and why does it matter?",
         "CI (Continuous Integration): automatically test and build on every push — catch bugs before merge. CD (Continuous Deployment): automatically deploy passing builds to production. Together: push code → tests run → build → deploy. No manual steps, no human error.",
         "# .github/workflows/deploy.yml\nname: CI/CD Pipeline\non:\n  push:\n    branches: [main]\njobs:\n  test-and-deploy:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-node@v4\n        with: { node-version: '20' }\n      - run: npm ci\n      - run: npm test\n      - run: npm run build\n      - name: Deploy\n        run: |\n          ssh user@server 'cd /app &&\n            git pull && npm ci &&\n            npm run build &&\n            pm2 restart all'",
         "Never deploy to production without automated tests passing in CI."),

        ("INTERMEDIATE", 5, "What is load balancing? Explain load balancing algorithms.",
         "Load balancing distributes requests across multiple servers to prevent overload. Algorithms: Round Robin (rotate equally), Least Connections (route to least busy), IP Hash (consistent routing per user), Weighted (more traffic to stronger servers).",
         "# Nginx load balancer config\nupstream backend {\n  least_conn;\n\n  server app1.example.com:3000 weight=3;\n  server app2.example.com:3000 weight=2;\n  server app3.example.com:3000 weight=1;\n\n  keepalive 32;\n}\n\nserver {\n  listen 80;\n  location / {\n    proxy_pass http://backend;\n    proxy_set_header Host $host;\n    proxy_set_header X-Real-IP $remote_addr;\n    proxy_connect_timeout 5s;\n    proxy_read_timeout 30s;\n  }\n}",
         "Nginx, HAProxy (open source), AWS ALB, GCP Load Balancer, Cloudflare are popular options."),

        ("INTERMEDIATE", 5, "How does Redis work as a cache? Explain eviction policies.",
         "Redis is an in-memory key-value store with sub-millisecond latency. When memory fills up, eviction policies decide what to remove. allkeys-lru (Least Recently Used) is the standard cache policy — evicts least-used keys regardless of TTL. volatile-lru only evicts keys that have a TTL set.",
         "const redis = require('ioredis');\nconst client = new redis(process.env.REDIS_URL);\n\n// Set with 1-hour TTL\nawait client.setex('product:123', 3600,\n  JSON.stringify(product));\n\n// Get\nconst raw = await client.get('product:123');\nif (raw) return JSON.parse(raw);\n\n// Atomic operations\nawait client.incr('page:views:home');\nawait client.lpush('recent:products', productId);\nawait client.ltrim('recent:products', 0, 9); // keep 10",
         "Set maxmemory and maxmemory-policy in redis.conf. allkeys-lru is the standard cache policy."),

        ("INTERMEDIATE", 4, "What are message queues and when should you use them?",
         "Message queues decouple producers from consumers for async processing. Use when: tasks are slow (email, video encoding), you need retry logic, you need to absorb traffic spikes, or services should be loosely coupled. The queue buffers work and guarantees delivery.",
         "const { Queue, Worker } = require('bullmq');\n\n// Producer — add to queue\nconst emailQueue = new Queue('email', { connection: redis });\n\nawait emailQueue.add('welcome', { userId }, {\n  attempts: 3,\n  backoff: { type: 'exponential', delay: 1000 }\n});\n\n// Consumer — process jobs\nnew Worker('email', async job => {\n  const { userId } = job.data;\n  const user = await db.findById(userId);\n  await mailer.sendWelcome(user.email);\n}, { connection: redis });",
         "BullMQ (Redis-based) is great for Node.js. For massive event streaming, use Apache Kafka."),

        ("INTERMEDIATE", 4, "Explain the production infrastructure flow for a scalable app.",
         "Request journey: User → CDN (edge cache) → Load Balancer → App Servers (stateless) → Cache Layer (Redis) → Database (primary writes / replica reads). Background jobs flow through message queues to workers. Each layer can scale independently.",
         "// Production flow:\n// 1. User hits CDN (Cloudflare/CloudFront)\n//    -> cached: serve immediately\n//    -> miss: forward to origin\n\n// 2. Load Balancer (Nginx/AWS ALB)\n//    -> distributes to app server pool\n\n// 3. App Server (stateless Next.js/Node)\n//    -> check Redis cache\n//    -> cache hit: return immediately\n//    -> cache miss: query PostgreSQL replica\n//    -> write operations: PostgreSQL primary\n\n// 4. Background tasks:\n//    -> BullMQ/Kafka -> Workers\n//    -> (email, notifications, analytics)",
         "Always make app servers stateless — store sessions, cache, and feature flags in Redis."),

        ("INTERMEDIATE", 4, "Explain blue-green vs canary deployments.",
         "Blue-green: two identical environments — Blue (current) and Green (new). Deploy to Green, test it, then switch traffic instantly. Instant rollback by switching back. Canary: gradually route a small percentage of traffic (1%, 5%, 25%...) to the new version. Monitor metrics at each step. Roll back if errors spike.",
         "// Blue-green deployment\n// 1. Deploy new version to 'green' servers\n// 2. Run smoke tests on green\n// 3. Switch load balancer to green\n// 4. Old 'blue' becomes standby\n// Rollback: switch LB back to blue\n\n// Canary deployment\n// 1. Deploy new version to 1 server\n// 2. Route 5% traffic to canary\n// 3. Monitor error rate, latency, p99\n// 4. If healthy: increase to 25% -> 50% -> 100%\n// 5. If unhealthy: route 100% back to old\n\n// Nginx canary\nupstream backend {\n  server old-v1:3000 weight=95;\n  server new-v2:3000 weight=5;\n}",
         "Blue-green is simpler. Canary is safer for large-scale systems with millions of users."),

        ("INTERMEDIATE", 4, "What is serverless architecture?",
         "Serverless means you write functions, the cloud runs them — no server management. You pay only for execution time (not idle servers). AWS Lambda, Vercel Edge Functions, Cloudflare Workers. Trade-offs: cold starts, execution time limits, vendor lock-in, harder debugging.",
         "// AWS Lambda function\nexport const handler = async (event) => {\n  const { userId } = JSON.parse(event.body);\n  const user = await db.findUser(userId);\n  return {\n    statusCode: 200,\n    body: JSON.stringify(user),\n  };\n};\n\n// Vercel Edge Function\nexport const config = { runtime: 'edge' };\nexport default function handler(req) {\n  return new Response(JSON.stringify({ hello: 'world' }), {\n    headers: { 'Content-Type': 'application/json' },\n  });\n}",
         "Serverless is great for: APIs, webhooks, cron jobs, image processing. Bad for: long-running tasks, WebSockets."),

        ("INTERMEDIATE", 3, "Explain feature flags and progressive rollouts.",
         "Feature flags let you deploy code with features hidden behind toggles — enable for specific users, percentages, or environments without redeploying. Progressive rollout: enable for internal team → beta users → 10% → 50% → 100%. If something breaks, disable the flag instantly.",
         "// Simple feature flag\nif (featureFlags.isEnabled('new-checkout', user)) {\n  return <NewCheckout />;\n} else {\n  return <OldCheckout />;\n}\n\n// With LaunchDarkly / Unleash\nconst showFeature = ldClient.variation(\n  'new-checkout',\n  { key: user.id, email: user.email },\n  false // default\n);\n\n// Rollout rules:\n// - Internal team: 100%\n// - Beta users: 100%\n// - Production: 10% (gradually increase)",
         "Feature flags decouple deployment from release — deploy daily, release when ready."),

        ("ADVANCED", 4, "What is Kubernetes and how does it orchestrate containers?",
         "Kubernetes (K8s) manages containers at scale: scheduling across nodes, self-healing (restarts failed pods), rolling deployments (zero downtime), HPA (auto-scaling based on metrics), service discovery, load balancing, and secret management. It's the industry standard for container orchestration.",
         "# deployment.yaml\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: api\nspec:\n  replicas: 3\n  selector:\n    matchLabels: { app: api }\n  template:\n    spec:\n      containers:\n      - name: api\n        image: myregistry/api:v1.2.3\n        resources:\n          requests: { cpu: 100m, memory: 128Mi }\n          limits: { cpu: 500m, memory: 512Mi }\n---\n# Auto-scale 3-20 pods based on CPU\napiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nspec:\n  minReplicas: 3\n  maxReplicas: 20\n  metrics:\n  - type: Resource\n    resource:\n      name: cpu\n      target:\n        type: Utilization\n        averageUtilization: 70",
         "Start with Docker Compose for local dev. Graduate to Kubernetes when managing 5+ services."),

        ("ADVANCED", 4, "How would you design a system for 1 million concurrent users?",
         "Layer the architecture: CDN → Load Balancer → Stateless App Servers (auto-scaling) → Redis Cache Cluster → DB (primary + read replicas) → Message Queues → Background Workers → Monitoring. Key: estimate capacity first, then design each layer to handle it.",
         "// Capacity estimation for 1M users:\n// Peak: ~50K req/sec (assume 5% concurrent)\n// Avg response: 100ms -> 5000 RPS per server\n// -> Need ~10 app servers at peak\n// DB reads: 80% -> route to 3 replicas\n// DB writes: 20% -> primary\n// Cache hit rate target: 95%+\n\n// Auto-scaling rule:\n// Scale out when CPU > 70% for 2 minutes\n// Scale in when CPU < 30% for 5 minutes\n// Min: 3 instances (HA)\n// Max: 50 instances (cost cap)",
         "Always estimate: traffic → server count → DB connections → cache hit rate → infrastructure cost."),

        ("ADVANCED", 4, "Explain distributed tracing and observability.",
         "Observability has 3 pillars: Metrics (numbers — Prometheus/Grafana), Logs (text — centralized logging), Traces (request journeys — distributed tracing). Distributed tracing tracks a request across services using a shared trace ID. Use OpenTelemetry as the standard instrumentation.",
         "// OpenTelemetry setup\nconst { trace } = require('@opentelemetry/api');\n\nasync function processOrder(orderId) {\n  const tracer = trace.getTracer('order-service');\n  const span = tracer.startSpan('processOrder');\n  span.setAttribute('order.id', orderId);\n\n  try {\n    const order = await db.findOrder(orderId);\n    span.addEvent('order.fetched');\n\n    await paymentService.charge(order);\n    span.setStatus({ code: SpanStatusCode.OK });\n  } catch (err) {\n    span.recordException(err);\n    span.setStatus({ code: SpanStatusCode.ERROR });\n    throw err;\n  } finally {\n    span.end();\n  }\n}",
         "Key SLIs to monitor: latency (p50/p95/p99), error rate (%), throughput (RPS), saturation (CPU/mem)."),

        ("ADVANCED", 4, "What is the Saga pattern in microservices?",
         "Saga manages distributed transactions across microservices — each service has its own database, so no global SQL transactions. Two flavors: Choreography (services emit events that trigger next steps) vs Orchestration (a central coordinator calls each service). On failure, compensating transactions undo completed steps.",
         "// Orchestration Saga\nclass OrderSaga {\n  async execute(orderId) {\n    try {\n      await inventoryService.reserve(orderId);\n      await paymentService.charge(orderId);\n      await shippingService.schedule(orderId);\n      await notifyService.send(orderId);\n    } catch (err) {\n      // Compensate — rollback in reverse\n      await shippingService.cancel(orderId);\n      await paymentService.refund(orderId);\n      await inventoryService.release(orderId);\n      throw err;\n    }\n  }\n}",
         "Compensating transactions are the microservices equivalent of SQL ROLLBACK."),

        ("ADVANCED", 3, "What is Infrastructure as Code (IaC)?",
         "IaC manages infrastructure (servers, networks, databases) through code files instead of manual configuration. Benefits: version controlled, reproducible, reviewable, automated. Terraform is cloud-agnostic. Pulumi uses real programming languages. AWS CDK is AWS-specific.",
         "# Terraform — provision AWS resources\nresource \"aws_instance\" \"api_server\" {\n  ami           = \"ami-0c55b159cbfafe1f0\"\n  instance_type = \"t3.medium\"\n  tags = { Name = \"api-server\" }\n}\n\nresource \"aws_rds_instance\" \"postgres\" {\n  engine         = \"postgres\"\n  engine_version = \"15.4\"\n  instance_class = \"db.t3.medium\"\n  allocated_storage = 100\n  multi_az       = true\n}\n\n# Apply changes\n# terraform plan  (preview)\n# terraform apply (execute)",
         "Never configure production infrastructure manually — use IaC for everything."),

        ("ADVANCED", 3, "Explain secrets management in production.",
         "Never store secrets in code, env files, or git. Use dedicated secret managers: AWS Secrets Manager, HashiCorp Vault, Google Secret Manager. They provide encryption, access control, rotation, and audit logging. Rotate secrets regularly and grant least-privilege access.",
         "// AWS Secrets Manager\nconst { SecretsManager } = require('@aws-sdk/client-secrets-manager');\nconst client = new SecretsManager({ region: 'us-east-1' });\n\nasync function getSecret(name) {\n  const response = await client.getSecretValue({\n    SecretId: name\n  });\n  return JSON.parse(response.SecretString);\n}\n\nconst dbCreds = await getSecret('prod/database');\n// { host, port, username, password }\n\n// Kubernetes secrets\n// kubectl create secret generic db-creds \\\n//   --from-literal=password=xxx",
         "Rotate secrets regularly. If a secret is exposed, rotate ALL related credentials immediately."),

        ("ADVANCED", 3, "What are common production engineering mistakes to avoid?",
         "7 deadly sins: 1) No monitoring — blind when things break. 2) Hardcoded secrets — security breach waiting to happen. 3) No rate limiting — open to brute force. 4) Unhandled promise rejections — crash Node processes. 5) No backups — catastrophic data loss. 6) No CI/CD — error-prone manual deploys. 7) Premature microservices.",
         "// Handle all unhandled rejections\nprocess.on('unhandledRejection', (reason, promise) => {\n  logger.error('Unhandled rejection:', reason);\n  // Graceful shutdown\n  server.close(() => process.exit(1));\n});\n\n// Validate env vars on startup\nconst required = ['DB_URL','JWT_SECRET','REDIS_URL'];\nfor (const key of required) {\n  if (!process.env[key])\n    throw new Error(key + ' env var not set');\n}\n\n// Graceful shutdown\nprocess.on('SIGTERM', async () => {\n  await server.close();\n  await db.end();\n  process.exit(0);\n});",
         "Add a production readiness checklist: monitoring, logging, backups, secrets, rate limits, graceful shutdown."),

        ("INTERMEDIATE", 4, "Explain the Twelve-Factor App methodology.",
         "A methodology for building modern, scalable, cloud-native SaaS applications. Key factors: 1) Codebase: one repo, many deploys. 2) Dependencies: explicitly declare/isolate. 3) Config: store in environment. 4) Backing services: treat as attached resources. 6) Processes: stateless, share-nothing. 9) Disposability: fast startup and graceful shutdown. 11) Logs: treat as streams.",
         "// Factor 3: Config in env (good)\nconst dbUrl = process.env.DATABASE_URL;\n\n// Factor 9: Disposability (graceful shutdown on SIGTERM)\nprocess.on('SIGTERM', () => {\n  server.close(() => {\n    db.disconnect();\n    process.exit(0);\n  });\n});",
         "Adhering to the Twelve-Factor App methodology ensures portability, scalability, and ease of deployment in containerized environments."),

        ("ADVANCED", 3, "What is GitOps and how does it differ from traditional CI/CD?",
         "GitOps is an operational framework where Git is the single source of truth for declarative infrastructure and applications. In traditional CI/CD, the CI pipeline runs a script to push changes to the cluster (push-based). In GitOps, an agent running inside the cluster (like ArgoCD or Flux) continuously pulls the declarative state from Git and reconciles differences (pull-based). This is more secure and prevents configuration drift.",
         "# gitops/argo-app.yaml (ArgoCD Application Definition)\napiVersion: argoproj.io/v1alpha1\nkind: Application\nspec:\n  source:\n    repoURL: 'https://github.com/org/infra-gitops.git'\n    path: k8s/production\n  destination:\n    server: 'https://kubernetes.default.svc'\n    namespace: default\n  syncPolicy:\n    automated: { prune: true, selfHeal: true }",
         "GitOps keeps your cluster configuration sync automatic, self-healing, and fully auditable via git commit logs."),

        ("ADVANCED", 4, "Explain high availability (HA) and multi-region active-active deployments.",
         "HA ensures a system remains operational with minimal downtime (aiming for 99.99% 'four nines'). Multi-region active-active deployment means running identical fully-functioning application stack instances in multiple geographical locations (regions) simultaneously, routing traffic using latency-based DNS. This protects against entire cloud region failures and provides low-latency access globally. It requires a distributed, replicated database.",
         "// Route 53 latency routing JSON config (conceptual DNS record)\n{\n  \"Name\": \"api.myapp.com\",\n  \"Type\": \"A\",\n  \"SetIdentifier\": \"us-east-instance\",\n  \"Region\": \"us-east-1\",\n  \"AliasTarget\": { \"DNSName\": \"us-elb.myapp.com\" }\n}\n// Route 53 handles routing based on client round-trip-time dynamically.",
         "Active-active requires databases designed for distributed writes (like CockroachDB, Spanner, or DynamoDB with Global Tables)."),

        ("INTERMEDIATE", 4, "Explain the differences between gRPC and REST/GraphQL.",
         "REST and GraphQL use JSON over HTTP/1.1 (human-readable, text-based, high overhead). gRPC (Google Remote Procedure Call) uses Protocol Buffers (Protobuf) over HTTP/2 (binary-serialized, highly compact, multiplexed connections). gRPC is schema-first (defined in .proto files) and supports bidirectional streaming. It is ideal for internal microservices communication, but harder to consume from web browsers directly.",
         "// user.proto\nsyntax = \"proto3\";\n\nmessage UserRequest { string id = 1; }\nmessage UserResponse { string id = 1; string name = 2; }\n\nservice UserService {\n  rpc GetUser (UserRequest) returns (UserResponse);\n}",
         "Use gRPC for fast, type-safe communication between internal microservices. Use REST or GraphQL for client-facing public APIs."),

        ("ADVANCED", 3, "What is Service Mesh (e.g. Istio) and when do you need it?",
         "A service mesh is a dedicated infrastructure layer for handling service-to-service communication in microservices. It deploys a proxy (like Envoy) as a 'sidecar' next to every service container. The sidecars intercept all network traffic, providing: mutual TLS (mTLS) encryption automatically, traffic splitting (canary routing), rate limiting, distributed tracing injection, and circuit breaking without modifying application code.",
         "# Istio VirtualService for canary deployment (traffic routing)\napiVersion: networking.istio.io/v1alpha3\nkind: VirtualService\nspec:\n  hosts: [ \"payment-service\" ]\n  http:\n    - route:\n        - destination: { host: \"payment-service\", subset: \"v1\" }\n          weight: 90\n        - destination: { host: \"payment-service\", subset: \"v2\" }\n          weight: 10",
         "A service mesh is usually overkill for small systems, but becomes critical as you scale to dozens of microservices."),

        ("ADVANCED", 4, "Explain CDN Edge Computing vs traditional serverless functions.",
         "Traditional serverless (AWS Lambda) runs in a single region, spins up a micro-VM (cold start up to seconds), and supports full Node.js runtime. Edge computing (Vercel Edge, Cloudflare Workers) runs inside CDN edge nodes globally, starts instantly (zero cold start using V8 isolates instead of VMs), but uses a subset of standard Web APIs (no node:fs or child_process). Edge is perfect for low-latency tasks like redirects, headers, or streaming AI.",
         "// Edge function (Vercel Edge Runtime / Web APIs)\nexport const config = { runtime: 'edge' };\n\nexport default async function handler(req) {\n  const geo = req.geo?.country || 'US';\n  if (geo === 'BD') {\n    return Response.redirect(new URL('/bd', req.url));\n  }\n  return new Response(JSON.stringify({ hello: 'world' }), {\n    headers: { 'Content-Type': 'application/json' }\n  });\n}",
         "Use the Edge Runtime for dynamic features that need near-zero latency, like localized routing or dynamic personalization."),

        ("ADVANCED", 3, "How do you handle log aggregation at scale?",
         "Do not write log files to server disks — logs should be treated as continuous streams written to stdout/stderr. An agent (FluentBit, Vector, Logstash) running on the host/pod intercepts these streams, parses the JSON structure, buffers them, and ships them to a centralized indexing cluster (Elasticsearch/OpenSearch, Grafana Loki, Datadog) where they can be queried.",
         "# Vector configuration snippet (collecting stdout & sending to Loki)\nsources:\n  docker_logs:\n    type: docker_logs\nsinks:\n  loki_output:\n    type: loki\n    inputs: [ \"docker_logs\" ]\n    endpoint: \"http://loki:3100\"\n    labels: { environment: \"production\", service: \"{{ container_name }}\" }",
         "Structured logging (writing logs as JSON objects) is critical for easy indexing and querying in aggregation tools."),

        ("INTERMEDIATE", 3, "Explain disaster recovery strategies: RTO and RPO.",
         "Two key metrics in Disaster Recovery (DR) planning: RTO (Recovery Time Objective) — how fast you must recover after an outage (e.g. system must be back online within 4 hours). RPO (Recovery Point Objective) — how much data you can afford to lose, measured in time (e.g. RPO = 24 hours means you restore from yesterday's backup and lose up to 24 hours of writes). Lower RTO/RPO requires active database replication and failover.",
         "DR Tiering Strategies:\n- Backup & Restore: RTO = hours/days, RPO = 24 hours (cheap)\n- Pilot Light (DB replicated, core idle): RTO = minutes, RPO = minutes\n- Warm Standby (scaled-down active cluster): RTO = minutes, RPO = seconds\n- Multi-Site Active-Active: RTO = near-zero, RPO = zero (expensive)",
         "Test your disaster recovery plans and automated backups regularly. An untested recovery plan is not a recovery plan."),
    ],

    # =====================================================================
    "Phase 7: Testing & Quality Assurance": [
        ("BASIC", 5, "What is the difference between Unit, Integration, and E2E testing?",
         "Unit: tests a single function/component in isolation (fast, many). Integration: tests how multiple units work together (medium speed). E2E: simulates a real user in a real browser (slow, few). The Testing Pyramid: many unit tests at the base, fewer integration in the middle, fewest E2E at the top.",
         "// Unit\nexpect(sum(1, 2)).toBe(3);\n\n// Integration\nrender(<LoginForm />);\nuserEvent.type(screen.getByLabelText('Email'), 'test@test.com');\n\n// E2E\nawait page.goto('/login');\nawait page.fill('#email', 'test@test.com');",
         "The Testing Pyramid suggests many Unit tests, some Integration tests, and fewer E2E tests (as they are slow and brittle)."),

        ("BASIC", 5, "What is Test-Driven Development (TDD)?",
         "TDD is a 3-step cycle: Red (write a failing test first) → Green (write minimum code to pass) → Refactor (improve code while keeping tests green). It forces you to think about the API before implementation. Result: better design, fewer bugs, higher confidence.",
         "// 1. RED — write failing test\ntest('adds two numbers', () => {\n  expect(add(2, 3)).toBe(5);\n});\n// RUN: FAIL (add doesn't exist)\n\n// 2. GREEN — minimum code to pass\nfunction add(a, b) { return a + b; }\n// RUN: PASS\n\n// 3. REFACTOR — improve if needed\n// (already clean, move on to next test)\n\n// 4. Next test: edge cases\ntest('handles negative numbers', () => {\n  expect(add(-1, -2)).toBe(-3);\n});",
         "TDD isn't about testing — it's about design. Tests drive you to write modular, decoupled code."),

        ("BASIC", 4, "What is code coverage and what's a good target?",
         "Code coverage measures what percentage of your code is executed by tests. Types: line coverage, branch coverage (if/else), function coverage. 80% is a good practical target. 100% is usually not worth the effort — diminishing returns. Focus on critical path coverage, not vanity numbers.",
         "// Jest coverage report\n// npx jest --coverage\n\n// Output:\n// File        | Stmts | Branch | Funcs | Lines\n// ------------|-------|--------|-------|------\n// user.ts     | 95%   | 88%    | 100%  | 95%\n// auth.ts     | 82%   | 75%    | 90%   | 82%\n// utils.ts    | 100%  | 100%   | 100%  | 100%\n\n// jest.config.js\ncoverageThreshold: {\n  global: {\n    branches: 80,\n    functions: 80,\n    lines: 80,\n    statements: 80,\n  }\n}",
         "High coverage ≠ good tests. You can have 100% coverage with zero meaningful assertions."),

        ("INTERMEDIATE", 5, "Explain React Testing Library best practices.",
         "RTL tests behavior, not implementation. Query priority: getByRole > getByLabelText > getByPlaceholderText > getByText > getByTestId. Test what users see and do. Never test state directly — test the rendered output. Avoid testing implementation details that might change during refactoring.",
         "// Good — testing behavior\nrender(<Counter />);\nconst button = screen.getByRole('button', { name: /increment/i });\nfireEvent.click(button);\nexpect(screen.getByText('Count: 1')).toBeInTheDocument();\n\n// Bad — testing implementation\nwrapper.setState({ count: 1 });\nexpect(wrapper.state('count')).toBe(1);\n\n// Testing async\nrender(<UserProfile userId='1' />);\nconst name = await screen.findByText('Nazmul');\nexpect(name).toBeInTheDocument();",
         "Query by accessibility roles first (getByRole). It ensures your app is accessible too."),

        ("INTERMEDIATE", 5, "How do you mock API calls in tests?",
         "Use MSW (Mock Service Worker) to intercept network requests at the network level — works for both tests and local development. Unlike jest.mock, MSW doesn't require you to know which module makes the request. It mocks the network, not the code.",
         "import { http, HttpResponse } from 'msw';\nimport { setupServer } from 'msw/node';\n\nconst server = setupServer(\n  http.get('/api/user', () => {\n    return HttpResponse.json({ name: 'Nazmul' });\n  }),\n  http.post('/api/login', async ({ request }) => {\n    const body = await request.json();\n    if (body.password === 'correct')\n      return HttpResponse.json({ token: 'abc' });\n    return HttpResponse.json(\n      { error: 'Invalid' }, { status: 401 }\n    );\n  })\n);\n\nbeforeAll(() => server.listen());\nafterEach(() => server.resetHandlers());\nafterAll(() => server.close());",
         "MSW v2 is the industry standard for mocking APIs. It works with fetch, axios, and any HTTP client."),

        ("INTERMEDIATE", 4, "Compare Playwright vs Cypress for E2E testing.",
         "Cypress: runs in the browser, excellent DX, real-time reloading, time-travel debugging. Single browser tab limitation. Playwright: runs outside the browser (CDP/WebSocket), supports multiple tabs/browsers/contexts, better for complex flows. Playwright is more powerful; Cypress has better DX for simple flows.",
         "// Cypress\ncy.visit('/login');\ncy.get('[data-testid=email]').type('test@test.com');\ncy.get('[data-testid=password]').type('password');\ncy.get('button[type=submit]').click();\ncy.url().should('include', '/dashboard');\n\n// Playwright\nawait page.goto('/login');\nawait page.fill('[data-testid=email]', 'test@test.com');\nawait page.fill('[data-testid=password]', 'password');\nawait page.click('button[type=submit]');\nawait expect(page).toHaveURL(/dashboard/);",
         "Playwright for complex multi-page/multi-browser tests. Cypress for simpler, developer-focused E2E."),

        ("INTERMEDIATE", 4, "How do you test React hooks?",
         "Use @testing-library/react's renderHook to test custom hooks in isolation. It renders the hook inside a test component and gives you the result. For hooks that need providers (context, Redux), wrap with a custom wrapper.",
         "import { renderHook, act } from '@testing-library/react';\nimport { useCounter } from './useCounter';\n\ntest('increments counter', () => {\n  const { result } = renderHook(() => useCounter(0));\n\n  expect(result.current.count).toBe(0);\n\n  act(() => {\n    result.current.increment();\n  });\n\n  expect(result.current.count).toBe(1);\n});\n\n// With provider wrapper\nconst wrapper = ({ children }) => (\n  <AuthProvider>{children}</AuthProvider>\n);\nconst { result } = renderHook(() => useAuth(), { wrapper });",
         "Always wrap state updates in act() — it ensures React processes all updates before assertions."),

        ("INTERMEDIATE", 4, "How do you test async code in Jest?",
         "Three approaches: 1) Return a promise. 2) Use async/await (most common). 3) Use done callback (legacy). For timers, use jest.useFakeTimers(). Always handle both success and error paths. Use waitFor() in RTL for async DOM updates.",
         "// async/await (preferred)\ntest('fetches user data', async () => {\n  const user = await fetchUser(1);\n  expect(user.name).toBe('Nazmul');\n});\n\n// Testing errors\ntest('throws on invalid id', async () => {\n  await expect(fetchUser(-1))\n    .rejects.toThrow('Invalid ID');\n});\n\n// Fake timers\ntest('debounce waits before calling', () => {\n  jest.useFakeTimers();\n  const fn = jest.fn();\n  const debounced = debounce(fn, 500);\n\n  debounced();\n  expect(fn).not.toHaveBeenCalled();\n\n  jest.advanceTimersByTime(500);\n  expect(fn).toHaveBeenCalledTimes(1);\n});",
         "jest.useFakeTimers() is essential for testing debounce, throttle, and setTimeout logic."),

        ("INTERMEDIATE", 3, "What is snapshot testing?",
         "Snapshot testing captures the rendered output of a component and saves it to a file. On subsequent runs, it compares the current output against the saved snapshot. If they differ, the test fails — you decide if the change is intentional (update snapshot) or a bug (fix code).",
         "// Component snapshot\ntest('renders correctly', () => {\n  const tree = renderer.create(\n    <Button label='Click me' />\n  ).toJSON();\n  expect(tree).toMatchSnapshot();\n});\n\n// Inline snapshot (stored in test file)\ntest('renders greeting', () => {\n  const { container } = render(<Greeting name='Ali' />);\n  expect(container).toMatchInlineSnapshot(`\n    <div>\n      <h1>Hello, Ali!</h1>\n    </div>\n  `);\n});\n\n// Update snapshots: npx jest --updateSnapshot",
         "Snapshots catch unintended UI changes but can be noisy. Use sparingly for stable components."),

        ("INTERMEDIATE", 3, "Explain contract testing for APIs.",
         "Contract testing verifies that a producer (API) and consumer (frontend/service) agree on the request/response format. Unlike integration tests, each side tests independently against a shared contract. Tools: Pact, MSW. Prevents: 'the API changed and nobody told the frontend'.",
         "// Pact contract test (consumer side)\nconst interaction = {\n  state: 'user exists',\n  uponReceiving: 'a request for user 1',\n  withRequest: {\n    method: 'GET',\n    path: '/api/users/1',\n  },\n  willRespondWith: {\n    status: 200,\n    body: {\n      id: 1,\n      name: like('Nazmul'),  // type matching\n      email: like('test@test.com'),\n    }\n  }\n};\n\n// Provider verifies the same contract\n// If API changes break the contract, tests fail",
         "Contract tests are faster than E2E and catch integration issues between teams."),

        ("ADVANCED", 4, "How do you set up CI test strategies?",
         "Layer your CI pipeline: 1) Lint + type check (fastest, catch syntax issues). 2) Unit tests (fast, high coverage). 3) Integration tests (medium, test interactions). 4) E2E tests (slow, test critical paths only). Run fast checks first — fail fast, save CI minutes.",
         "# .github/workflows/test.yml\njobs:\n  lint:\n    steps:\n      - run: npm run lint\n      - run: npx tsc --noEmit\n\n  unit:\n    needs: lint\n    steps:\n      - run: npx jest --ci --coverage\n      - uses: codecov/codecov-action@v4\n\n  integration:\n    needs: unit\n    services:\n      postgres: { image: postgres:15 }\n      redis: { image: redis:7 }\n    steps:\n      - run: npm run test:integration\n\n  e2e:\n    needs: integration\n    steps:\n      - run: npx playwright test",
         "Run lint → unit → integration → E2E in order. Fail fast on cheap checks."),

        ("ADVANCED", 3, "What is visual regression testing?",
         "Visual regression testing captures screenshots of components/pages and compares them against baselines pixel-by-pixel. Catches CSS bugs, layout shifts, and unintended visual changes that functional tests miss. Tools: Chromatic (Storybook), Percy, Playwright visual comparisons.",
         "// Playwright visual comparison\ntest('homepage looks correct', async ({ page }) => {\n  await page.goto('/');\n  await expect(page).toHaveScreenshot('homepage.png', {\n    maxDiffPixelRatio: 0.01, // 1% tolerance\n  });\n});\n\n// Component-level with Storybook + Chromatic\n// 1. Write stories for each component state\n// 2. Chromatic captures screenshots in CI\n// 3. Visual diff on each PR\n// 4. Approve or reject changes\n\n// Update baselines:\n// npx playwright test --update-snapshots",
         "Visual tests catch the bugs that unit tests can't — like 'the button moved 2px left'."),

        ("ADVANCED", 3, "Explain load testing and performance testing.",
         "Load testing simulates many concurrent users to find breaking points. Key metrics: response time (p50, p95, p99), throughput (RPS), error rate. Tools: k6 (modern, JS-based), Artillery, JMeter. Run load tests against staging, never production.",
         "// k6 load test\nimport http from 'k6/http';\nimport { check, sleep } from 'k6';\n\nexport const options = {\n  stages: [\n    { duration: '1m', target: 100 },  // ramp up\n    { duration: '3m', target: 100 },  // sustain\n    { duration: '1m', target: 0 },    // ramp down\n  ],\n  thresholds: {\n    http_req_duration: ['p(95)<500'], // 95% under 500ms\n    http_req_failed: ['rate<0.01'],   // <1% errors\n  },\n};\n\nexport default function () {\n  const res = http.get('https://staging.myapp.com/api/products');\n  check(res, {\n    'status 200': (r) => r.status === 200,\n    'fast response': (r) => r.timings.duration < 500,\n  });\n  sleep(1);\n}",
         "k6 is developer-friendly (write tests in JS), runs locally or in the cloud, and has great reporting."),

        ("ADVANCED", 3, "Explain Mutation Testing and how it improves test suite quality.",
         "Mutation testing evaluates the quality of your tests by injecting small bugs (mutations) into your production code and running your test suite. If your tests fail, the mutation is 'killed' (good). If your tests pass, the mutation 'survived' (bad), indicating a gap in test coverage or assertions. Tools like Stryker Mutator automate this.",
         "// Original Code:\n// if (age >= 18) { return true; }\n\n// Mutated Code (Stryker injects mutation):\n// if (age > 18) { return true; } // Changed >= to >\n\n// If tests do not have a test case for age = 18,\n// the mutation survives. You must add a test case:\nexpect(isAdult(18)).toBe(true);",
         "High code coverage doesn't mean high quality. Mutation testing verifies that your assertions actually assert the correct behaviors."),

        ("INTERMEDIATE", 3, "What is Behavior-Driven Development (BDD)?",
         "TDD focuses on the developer's perspective (unit structure, APIs). BDD (Behavior-Driven Development) focuses on the user's perspective (behavior, business logic) using a common language that developers, QAs, and product managers can understand. It uses Given-When-Then format Gherkin syntax with tools like Cucumber.",
         "# BDD Feature spec (Gherkin syntax)\nFeature: User Login\n  Scenario: Successful login with valid credentials\n    Given the user is on the login page\n    When they enter 'test@user.com' and 'password123'\n    And click 'Submit'\n    Then they should see the dashboard page",
         "BDD helps align business requirements directly with automated tests, reducing communication gaps between teams."),

        ("ADVANCED", 4, "How do you test for security vulnerabilities in CI/CD?",
         "Implement three security testing layers: 1) SAST (Static Application Security Testing): scans code for patterns indicating security flaws (ESLint security, SonarQube). 2) Dependency Scanning (SCA): scans node_modules for known CVEs (npm audit, Snyk). 3) DAST (Dynamic Application Security Testing): tests running app by simulating attacks (OWASP ZAP).",
         "# GitHub Actions Security Scan workflow snippet\n- name: Run npm audit\n  run: npm audit --audit-level=high\n  \n- name: Run Snyk to check for vulnerabilities\n  uses: snyk/actions/node@master\n  env:\n    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}",
         "Automating dependency scans in CI/CD prevents importing packages with critical security flaws into production."),

        ("BASIC", 4, "Explain the AAA (Arrange-Act-Assert) pattern in testing.",
         "The AAA pattern is a standard structure for writing clean, readable, and maintainable unit tests. It divides a test into three distinct blocks: 1) Arrange: set up the target object, inputs, and mock behaviors. 2) Act: execute the function or component method under test. 3) Assert: verify that the output or state matches expectations.",
         "test('calculates total with tax', () => {\n  // Arrange\n  const cart = new ShoppingCart();\n  cart.addItem({ name: 'Book', price: 10 });\n  \n  // Act\n  const total = cart.calculateTotal(0.1); // 10% tax\n  \n  // Assert\n  expect(total).toBe(11);\n});",
         "Keep the three blocks separated by blank lines and avoid mixing setup with assertions to keep tests readable."),

        ("INTERMEDIATE", 4, "How do you mock modules, dates, and timers in Jest or Vitest safely?",
         "Use Jest/Vitest mocking utilities to isolate code. Mock modules using jest.mock(). Use jest.useFakeTimers() to control time, and reset mocks between tests using afterEach(jest.clearAllMocks) to prevent test interference. To mock dates, use jest.setSystemTime() so that new Date() is completely deterministic.",
         "// Mocking Date and Timers\nbeforeEach(() => {\n  jest.useFakeTimers();\n  jest.setSystemTime(new Date('2026-06-12'));\n});\n\nafterEach(() => {\n  jest.useRealTimers();\n});\n\ntest('sends reminder after 24 hours', () => {\n  triggerReminderTimer();\n  jest.advanceTimersByTime(24 * 60 * 60 * 1000);\n  expect(sendEmailMock).toHaveBeenCalled();\n});",
         "Always call useRealTimers() after testing timers to avoid disrupting other asynchronous tests in your suite."),

        ("INTERMEDIATE", 4, "Explain the testing trophy model vs the testing pyramid.",
         "The Testing Pyramid focuses heavily on unit tests, some integration, and very few E2E tests. The Testing Trophy (popularized by Kent C. Dodds) prioritizes Integration tests over unit tests. The trophy structure is: 1) Static (type checkers, linters), 2) Unit (isolated logic), 3) Integration (component rendering, API - widest part, best ROI), 4) End-to-End (critical user paths).",
         "// Testing Pyramid vs Testing Trophy\n// Pyramid: Unit (70%) -> Integration (20%) -> E2E (10%)\n// Trophy: Static (Linter/TS) -> Unit (Core Logic) -> Integration (Component/API) -> E2E (Critical Paths)\n// Integration tests provide the maximum ROI for web applications.",
         "Integration tests strike the best balance between execution speed and real-world confidence."),

        ("ADVANCED", 4, "How do you handle flaky tests in E2E environments?",
         "Flaky tests pass or fail randomly due to network delays, race conditions, or asynchronous renders. Fixes: 1) Playwright auto-waiting: don't use arbitrary sleeps (like sleep(3000)); instead, wait for specific DOM states or network responses (waitForSelector, expect(locator).toBeVisible()). 2) Isolation: ensure tests have independent, clean state. 3) Run retries in CI.",
         "// Bad - arbitrary sleep causes flakiness\nawait page.click('#submit');\nawait page.waitForTimeout(3000);\nexpect(await page.textContent('#status')).toBe('Success');\n\n// Good - locator auto-waits for condition\nawait page.click('#submit');\nconst status = page.locator('#status');\nawait expect(status).toHaveText('Success', { timeout: 5000 });",
         "Never use arbitrary hardcoded timeouts for waiting. Always wait for specific, verifiable DOM states or network endpoints."),
    ],

    # =====================================================================
    "Phase 8: API Design & GraphQL": [
        ("BASIC", 5, "What are REST API design best practices?",
         "REST rules: 1) Use nouns not verbs in URLs (/users not /getUsers). 2) Use HTTP methods correctly (GET=read, POST=create, PUT=replace, PATCH=update, DELETE=remove). 3) Use proper status codes. 4) Version your API. 5) Use consistent naming (plural nouns, kebab-case). 6) Support filtering, sorting, pagination.",
         "// Good REST design\nGET    /api/v1/users          // list users\nGET    /api/v1/users/123      // get user 123\nPOST   /api/v1/users          // create user\nPATCH  /api/v1/users/123      // update user 123\nDELETE /api/v1/users/123      // delete user 123\n\n// Filtering & pagination\nGET /api/v1/users?role=admin&sort=-createdAt&page=2&limit=20\n\n// Nested resources\nGET /api/v1/users/123/posts   // user's posts\nPOST /api/v1/users/123/posts  // create user's post",
         "APIs are contracts — breaking changes break clients. Version from day one."),

        ("BASIC", 5, "Explain HTTP status codes and when to use them.",
         "5 families: 1xx (info), 2xx (success), 3xx (redirect), 4xx (client error), 5xx (server error). Key codes to memorize: 200 OK, 201 Created, 204 No Content, 301 Moved Permanently, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 429 Too Many Requests, 500 Server Error.",
         "// Success\n200 — OK (GET, PUT, PATCH)\n201 — Created (POST)\n204 — No Content (DELETE)\n\n// Client errors\n400 — Bad Request (invalid input)\n401 — Unauthorized (not logged in)\n403 — Forbidden (no permission)\n404 — Not Found\n409 — Conflict (duplicate email)\n422 — Unprocessable Entity (validation failed)\n429 — Too Many Requests (rate limited)\n\n// Server errors\n500 — Internal Server Error\n502 — Bad Gateway\n503 — Service Unavailable",
         "Use 401 for 'who are you?' and 403 for 'I know who you are, but you can't do this'."),

        ("BASIC", 5, "What is the difference between GraphQL and REST?",
         "REST: multiple endpoints, fixed data shapes, over/under-fetching. GraphQL: single endpoint, client specifies exactly what data it needs, no over-fetching. REST is simpler for CRUD. GraphQL shines when: multiple clients need different data shapes, or you need data from multiple resources in one request.",
         "// REST — multiple requests, over-fetching\nGET /api/users/1        // gets ALL user fields\nGET /api/users/1/posts  // separate request\nGET /api/users/1/friends // another request\n\n// GraphQL — single request, exact data\nquery {\n  user(id: 1) {\n    name\n    email\n    posts(limit: 5) {\n      title\n    }\n    friends {\n      name\n    }\n  }\n}",
         "REST for simple CRUD APIs. GraphQL for complex, nested data with multiple consumers."),

        ("INTERMEDIATE", 5, "Explain API pagination: offset vs cursor.",
         "Offset-based: page=2&limit=20 (skip first 20, take next 20). Simple but slow on large datasets — DB must count all skipped rows. Cursor-based: after=lastItemId&limit=20 — uses an indexed field to seek directly. Much faster at scale. Always use cursor for infinite scroll or large datasets.",
         "// Offset pagination (simple, slow at scale)\nGET /api/posts?page=3&limit=20\n// SQL: SELECT * FROM posts LIMIT 20 OFFSET 40\n\n// Cursor pagination (fast, scalable)\nGET /api/posts?after=abc123&limit=20\n// SQL: SELECT * FROM posts\n//   WHERE created_at < cursor_timestamp\n//   ORDER BY created_at DESC LIMIT 20\n\n// Response includes cursor for next page\n{\n  data: [...],\n  pagination: {\n    hasMore: true,\n    nextCursor: 'xyz789'\n  }\n}",
         "Cursor pagination is O(1) regardless of page number. Offset pagination is O(n) for page n."),

        ("INTERMEDIATE", 5, "How do you handle API error responses consistently?",
         "Define a standard error response format and use it everywhere. Include: error code (machine-readable), message (human-readable), details (field-level errors for validation). Use consistent HTTP status codes. Never expose internal errors or stack traces to clients.",
         "// Standard error format\n{\n  \"error\": {\n    \"code\": \"VALIDATION_ERROR\",\n    \"message\": \"Request validation failed\",\n    \"details\": [\n      { \"field\": \"email\", \"message\": \"Invalid email format\" },\n      { \"field\": \"age\", \"message\": \"Must be >= 18\" }\n    ]\n  }\n}\n\n// Error handler middleware\napp.use((err, req, res, next) => {\n  const status = err.statusCode || 500;\n  res.status(status).json({\n    error: {\n      code: err.code || 'INTERNAL_ERROR',\n      message: err.message,\n      ...(process.env.NODE_ENV !== 'production' &&\n        { stack: err.stack })\n    }\n  });\n});",
         "Consistent error formats make client-side error handling predictable and debuggable."),

        ("INTERMEDIATE", 4, "What are API versioning strategies?",
         "Three approaches: URL versioning (/api/v1/users — most common, explicit), header versioning (Accept: application/vnd.api+json;version=1 — cleaner URLs), query param (?version=1 — easy but messy). URL versioning is the most common and recommended — it's explicit and cacheable.",
         "// URL versioning (recommended)\napp.use('/api/v1', v1Router);\napp.use('/api/v2', v2Router);\n\n// Header versioning\napp.use('/api/users', (req, res, next) => {\n  const version = req.headers['api-version'] || '1';\n  if (version === '2') return v2Controller(req, res);\n  return v1Controller(req, res);\n});\n\n// Deprecation strategy\nres.set('Deprecation', 'true');\nres.set('Sunset', 'Sat, 01 Jan 2026 00:00:00 GMT');\nres.set('Link', '</api/v2/users>; rel=\"successor-version\"');",
         "When deprecating an API version, give clients at least 6 months notice with Sunset headers."),

        ("INTERMEDIATE", 4, "Explain GraphQL schema design.",
         "Define types (what data exists), queries (how to read), mutations (how to write), and subscriptions (how to listen). Use strong typing, input types for mutations, enums for fixed values, and interfaces for shared fields. Design schema from the client's perspective, not the database.",
         "type User {\n  id: ID!\n  name: String!\n  email: String!\n  posts(limit: Int = 10): [Post!]!\n  role: Role!\n}\n\nenum Role { USER ADMIN MODERATOR }\n\ntype Post {\n  id: ID!\n  title: String!\n  author: User!\n  createdAt: DateTime!\n}\n\ninput CreatePostInput {\n  title: String!\n  content: String!\n}\n\ntype Query {\n  user(id: ID!): User\n  posts(cursor: String, limit: Int): PostConnection!\n}\n\ntype Mutation {\n  createPost(input: CreatePostInput!): Post!\n  deletePost(id: ID!): Boolean!\n}",
         "Design GraphQL schema from the client's needs, not the database structure."),

        ("INTERMEDIATE", 4, "What is the N+1 problem in GraphQL and how do you solve it?",
         "When resolving a list of items with nested fields, each nested field triggers a separate DB query. 10 users → 10 separate queries for their posts = 11 total. Solution: DataLoader batches and deduplicates queries into a single batch call per tick of the event loop.",
         "// Without DataLoader — N+1\n// Query: { users { name posts { title } } }\n// 1 query for users + N queries for posts\n\n// With DataLoader — batched\nconst postLoader = new DataLoader(async (userIds) => {\n  // One query for ALL user IDs\n  const posts = await db.posts.findMany({\n    where: { userId: { in: userIds } }\n  });\n  // Return posts grouped by userId\n  return userIds.map(id =>\n    posts.filter(p => p.userId === id)\n  );\n});\n\n// Resolver\nUser: {\n  posts: (user) => postLoader.load(user.id)\n}",
         "DataLoader is essential for any production GraphQL server — without it, performance is terrible."),

        ("INTERMEDIATE", 4, "What is tRPC and why is it popular?",
         "tRPC gives you end-to-end type safety between client and server WITHOUT code generation or schemas. Define procedures on the server with Zod validation, and the client gets full TypeScript autocompletion and type checking. No API layer needed — types flow automatically.",
         "// Server (tRPC router)\nconst appRouter = router({\n  getUser: publicProcedure\n    .input(z.object({ id: z.string() }))\n    .query(async ({ input }) => {\n      return db.user.findUnique({ where: { id: input.id } });\n    }),\n\n  createPost: protectedProcedure\n    .input(z.object({\n      title: z.string().min(1),\n      content: z.string(),\n    }))\n    .mutation(async ({ input, ctx }) => {\n      return db.post.create({\n        data: { ...input, authorId: ctx.user.id }\n      });\n    }),\n});\n\n// Client — full autocompletion!\nconst user = await trpc.getUser.query({ id: '1' });\nuser.name; // TypeScript knows this exists!",
         "tRPC is perfect for full-stack TypeScript apps where you control both client and server."),

        ("INTERMEDIATE", 3, "What is rate limiting and how do you implement it for APIs?",
         "Rate limiting controls how many requests a client can make in a time window. Prevents abuse, brute force attacks, and ensures fair usage. Common algorithms: Fixed Window (simple counter per time window), Sliding Window (smoother), Token Bucket (allows bursts). Return 429 with Retry-After header when limited.",
         "// Token bucket algorithm (conceptual)\nclass TokenBucket {\n  constructor(capacity, refillRate) {\n    this.tokens = capacity;\n    this.capacity = capacity;\n    this.refillRate = refillRate; // tokens per second\n    this.lastRefill = Date.now();\n  }\n  consume() {\n    this.refill();\n    if (this.tokens > 0) {\n      this.tokens--;\n      return true; // allowed\n    }\n    return false; // rate limited\n  }\n}\n\n// Response headers\nres.set('X-RateLimit-Limit', '100');\nres.set('X-RateLimit-Remaining', '42');\nres.set('X-RateLimit-Reset', '1623456789');\nres.set('Retry-After', '30'); // seconds",
         "Always include rate limit headers so clients can self-regulate."),

        ("INTERMEDIATE", 3, "Explain API documentation with OpenAPI/Swagger.",
         "OpenAPI (formerly Swagger) is the standard for documenting REST APIs. Define endpoints, parameters, request/response schemas, and authentication in YAML/JSON. Tools auto-generate interactive docs, client SDKs, and mock servers. Good docs reduce support burden and onboarding time.",
         "# openapi.yaml\nopenapi: 3.0.3\ninfo:\n  title: User API\n  version: 1.0.0\npaths:\n  /api/users:\n    get:\n      summary: List users\n      parameters:\n        - name: page\n          in: query\n          schema: { type: integer, default: 1 }\n      responses:\n        '200':\n          description: Success\n          content:\n            application/json:\n              schema:\n                type: array\n                items:\n                  $ref: '#/components/schemas/User'\ncomponents:\n  schemas:\n    User:\n      type: object\n      properties:\n        id: { type: integer }\n        name: { type: string }",
         "Use swagger-jsdoc to generate OpenAPI from JSDoc comments in your code."),

        ("ADVANCED", 4, "How do you design authentication for GraphQL?",
         "Authentication in GraphQL happens in the context, not in individual resolvers. Parse the JWT/session in the context function and pass the user to all resolvers. Authorization happens per-resolver or per-field using directives or middleware. Never put auth logic in the schema itself.",
         "// Context — parse auth once\nconst server = new ApolloServer({\n  typeDefs,\n  resolvers,\n  context: async ({ req }) => {\n    const token = req.headers.authorization?.split(' ')[1];\n    const user = token ? verifyJWT(token) : null;\n    return { user, db };\n  },\n});\n\n// Resolver — check auth\nconst resolvers = {\n  Mutation: {\n    createPost: (_, args, ctx) => {\n      if (!ctx.user) throw new AuthenticationError('Login required');\n      return ctx.db.post.create({\n        data: { ...args.input, authorId: ctx.user.id }\n      });\n    },\n  },\n};",
         "Use a directive (@auth) or middleware library to avoid repeating auth checks in every resolver."),

        ("ADVANCED", 4, "Explain GraphQL subscriptions for real-time data.",
         "Subscriptions let clients receive real-time updates via WebSocket. The client subscribes to an event, and the server pushes data whenever that event occurs. Used for: chat messages, live notifications, real-time dashboards. Subscriptions are the GraphQL equivalent of WebSocket events.",
         "// Schema\ntype Subscription {\n  messageAdded(roomId: ID!): Message!\n  userTyping(roomId: ID!): User!\n}\n\n// Server resolver\nSubscription: {\n  messageAdded: {\n    subscribe: (_, { roomId }) =>\n      pubsub.asyncIterator(`ROOM_${roomId}`)\n  }\n}\n\n// Publish from mutation\nMutation: {\n  sendMessage: async (_, { roomId, text }, ctx) => {\n    const msg = await db.messages.create(...);\n    pubsub.publish(`ROOM_${roomId}`, {\n      messageAdded: msg\n    });\n    return msg;\n  }\n}\n\n// Client\nconst SUB = gql`\n  subscription OnMessage($roomId: ID!) {\n    messageAdded(roomId: $roomId) { text author { name } }\n  }\n`;",
         "Use Redis PubSub adapter for subscriptions across multiple server instances."),

        ("ADVANCED", 3, "Explain webhook design patterns.",
         "Webhooks are HTTP callbacks — your server calls the client's URL when an event occurs (reverse of polling). Design: register a URL, send POST with signed payload on events, expect 2xx acknowledgment, retry with exponential backoff on failure. Always verify webhook signatures.",
         "// Webhook sender\nasync function sendWebhook(url, event, payload) {\n  const body = JSON.stringify({ event, data: payload, ts: Date.now() });\n  const signature = crypto\n    .createHmac('sha256', secret)\n    .update(body).digest('hex');\n\n  await fetch(url, {\n    method: 'POST',\n    headers: {\n      'Content-Type': 'application/json',\n      'X-Webhook-Signature': signature,\n    },\n    body,\n  });\n}\n\n// Webhook receiver (verification)\napp.post('/webhooks/stripe', (req, res) => {\n  const sig = req.headers['stripe-signature'];\n  const event = stripe.webhooks.constructEvent(\n    req.body, sig, endpointSecret\n  );\n  // Process event...\n  res.json({ received: true });\n});",
         "Always verify webhook signatures — unsigned webhooks can be spoofed by attackers."),

        ("ADVANCED", 3, "What is API gateway pattern and why is it important?",
         "API gateway is the single entry point for all API requests. It handles cross-cutting concerns: authentication, rate limiting, request routing, response aggregation, protocol translation, and logging. Without it, every microservice must implement these concerns independently.",
         "// API Gateway responsibilities:\n// Client -> API Gateway -> Microservices\n//\n// 1. Authentication: verify JWT once\n// 2. Rate limiting: per user/API key\n// 3. Routing: /users -> user-service\n// 4. Aggregation: combine responses\n// 5. Caching: cache frequent reads\n// 6. Transformation: REST -> gRPC\n// 7. Monitoring: log all requests\n\n// Popular gateways:\n// - Kong (open source, plugin-based)\n// - AWS API Gateway (managed)\n// - Nginx (reverse proxy + gateway)\n// - Express Gateway (Node.js native)",
         "API gateway simplifies clients — they talk to one endpoint instead of discovering many services."),

        ("ADVANCED", 4, "Explain the Idempotency pattern in API design and how to implement it.",
         "An idempotent operation is one that produces the same result no matter how many times it is executed. GET, PUT, and DELETE are naturally idempotent. POST is not. To make POST (e.g., payment creation) idempotent: 1) Client sends a unique UUID in the Idempotency-Key header. 2) Server checks if this key exists in Redis. 3) If it exists, returns the cached response. 4) If not, acquires a lock, processes the request, stores the response in Redis with an expiration, and returns the response.",
         "app.post('/payments', async (req, res) => {\n  const key = req.headers['idempotency-key'];\n  if (!key) return res.status(400).send('Missing Idempotency-Key');\n  \n  const cached = await redis.get(key);\n  if (cached) return res.json(JSON.parse(cached));\n  \n  // Process payment...\n  const response = await processPayment(req.body);\n  await redis.set(key, JSON.stringify(response), 'EX', 86400); // 24h\n  return res.json(response);\n});",
         "Implementing idempotency keys is essential for critical write operations (like financial payments) to prevent duplicate transactions on network retries."),

        ("INTERMEDIATE", 3, "What is HATEOAS in REST API design and is it practical?",
         "HATEOAS (Hypermedia As The Engine Of Application State) is a constraint of REST. It states that the API response should return not just data, but also links to actions/related endpoints the client can take next, making the API self-documenting. In practice, it is rarely fully implemented because it adds considerable response payload size and development complexity, and frontends usually hardcode navigation paths anyway.",
         "// HATEOAS response example\n{\n  \"id\": 123,\n  \"name\": \"Nazmul\",\n  \"_links\": {\n    \"self\": { \"href\": \"/api/users/123\" },\n    \"posts\": { \"href\": \"/api/users/123/posts\" },\n    \"delete\": { \"href\": \"/api/users/123\", \"method\": \"DELETE\" }\n  }\n}",
         "While HATEOAS is a key constraint for level 3 REST maturity, most production systems use simpler REST APIs documented via OpenAPI/Swagger."),

        ("ADVANCED", 4, "Explain GraphQL schema stitching vs Apollo Federation.",
         "Both merge multiple sub-schemas into a single gateway schema. Schema Stitching: imperatively merges schemas at the gateway level using resolvers (requires gateway updates when sub-schemas change). Apollo Federation: declaratively composes schemas using subgraphs. Each subgraph defines its own schema and specifies how entities (types shared across services) are extended. The gateway automatically composes the schema dynamically.",
         "# Subgraph A (User Service)\ntype User @key(fields: \"id\") { id: ID! name: String! }\n\n# Subgraph B (Review Service)\nextend type User @key(fields: \"id\") {\n  id: ID! @external\n  reviews: [Review!]!\n}",
         "Apollo Federation is the modern enterprise standard for building a unified graph (Supergraph) across independent team microservices."),

        ("ADVANCED", 4, "How do you protect GraphQL APIs from abuse?",
         "Because GraphQL lets clients query arbitrary nested fields, malicious clients can crash servers. Protections: 1) Query Depth Limiting: inspect AST and reject queries exceeding a max depth. 2) Query Cost Analysis: assign costs to fields (scalar=1, list=5) and reject queries exceeding a max score. 3) Rate Limiting: limit based on total query complexity score per IP.",
         "import depthLimit from 'graphql-depth-limit';\nimport { createComplexityLimitRule } from 'graphql-validation-complexity';\n\nconst server = new ApolloServer({\n  typeDefs,\n  resolvers,\n  validationRules: [\n    depthLimit(5),\n    createComplexityLimitRule(1000)\n  ]\n});",
         "Always define query depth and complexity limits in production GraphQL servers to prevent Denial of Service (DoS) attacks."),

        ("INTERMEDIATE", 4, "Explain HTTP Caching headers and how they optimize API performance.",
         "1) Cache-Control: directs caches (browsers, CDNs) how to cache (public, max-age=3600). 2) ETag (Entity Tag): a unique hash representing the response content. The client sends it back in the If-None-Match header. If content hasn't changed, the server returns 304 Not Modified with no body. 3) Last-Modified: date of last modification, returned with If-Modified-Since.",
         "app.get('/api/resource', (req, res) => {\n  const content = getResource();\n  const etag = generateHash(content);\n  \n  if (req.headers['if-none-match'] === etag) {\n    return res.status(304).end(); // Not Modified\n  }\n  \n  res.set('ETag', etag);\n  res.set('Cache-Control', 'public, max-age=60'); // cache 60s\n  res.json(content);\n});",
         "ETags save bandwidth and CPU by avoiding database queries and JSON serialization when data has not changed since the last request."),
    ],
}

# --------------------------------------------------------------------------
# PDF Builder
# --------------------------------------------------------------------------

def stars_text(rating, max_rating=5):
    """Return styled HTML stars for the given rating."""
    filled = '<font color="#D4A017">\u2605</font>' * rating
    empty  = '<font color="#D6D0C0">\u2605</font>' * (max_rating - rating)
    return filled + empty

def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#888780'))

    # First line: Guide title and page number
    canvas.drawCentredString(W/2, 15*mm,
        f"Full-Stack Developer Interview Guide  |  Page {doc.page}")

    # Second line: Author details
    canvas.setFont('Helvetica-Oblique', 7)
    canvas.drawCentredString(W/2, 11*mm,
        "Curated by N.I. Nazmul — Full-Stack Developer (MERN Stack & Next.js Specialist)  |  https://github.com/ninazmul")

    canvas.restoreState()

def build_cover(story):
    story.append(Spacer(1, 25*mm))

    title_s = ParagraphStyle('t1', fontName='Helvetica-Bold', fontSize=36,
        leading=42, textColor=NAVY, alignment=TA_CENTER)
    sub_s = ParagraphStyle('t2', fontName='Helvetica', fontSize=16,
        leading=22, textColor=BLUE, alignment=TA_CENTER, spaceAfter=8)
    meta_s = ParagraphStyle('t3', fontName='Helvetica-Bold', fontSize=11,
        leading=15, textColor=DGRAY, alignment=TA_CENTER)
    meta_light = ParagraphStyle('t4', fontName='Helvetica', fontSize=10,
        leading=14, textColor=GRAY, alignment=TA_CENTER)

    author_title = ParagraphStyle('a1', fontName='Helvetica-Bold', fontSize=14,
        leading=18, textColor=TEAL, alignment=TA_CENTER)
    author_sub = ParagraphStyle('a2', fontName='Helvetica-Oblique', fontSize=11,
        leading=15, textColor=GRAY, alignment=TA_CENTER)

    story.append(Paragraph("Full-Stack Developer", title_s))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Interview Preparation Guide", sub_s))

    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width='60%', thickness=1.5, color=BORDER, hAlign='CENTER'))
    story.append(Spacer(1, 8*mm))

    # Count total questions
    total_q = sum(len(qs) for qs in QNA.values())

    story.append(Paragraph("MERN Stack &amp; Next.js  |  All Levels — Junior to Senior", meta_s))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(f"8 Phases  |  {total_q} Questions  |  Rated by Interview Frequency", meta_light))

    story.append(Spacer(1, 12*mm))

    # Author Info
    story.append(Paragraph("Curated by N.I. Nazmul", author_title))
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph("Full-Stack Developer (MERN Stack &amp; Next.js Specialist)", author_sub))
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph("github.com/ninazmul", author_sub))

    story.append(Spacer(1, 10*mm))

    # Legend
    legend_title_s = ParagraphStyle('lt', fontName='Helvetica-Bold', fontSize=10,
        leading=13, textColor=DGRAY, alignment=TA_CENTER)
    legend_s = ParagraphStyle('lg', fontName='Helvetica', fontSize=9,
        leading=13, textColor=GRAY, alignment=TA_CENTER)
    story.append(Paragraph("How to Read This Guide", legend_title_s))
    story.append(Spacer(1, 2*mm))

    legend_data = [
        [Paragraph('<font color="#3B6D11"><b>BASIC</b></font>', legend_s),
         Paragraph('<font color="#185FA5"><b>INTERMEDIATE</b></font>', legend_s),
         Paragraph('<font color="#993C1D"><b>ADVANCED</b></font>', legend_s)],
    ]
    legend_tbl = Table(legend_data, colWidths=[(W - 40*mm) / 3] * 3)
    legend_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,-1), LGREEN),
        ('BACKGROUND', (1,0), (1,-1), LBLUE),
        ('BACKGROUND', (2,0), (2,-1), LCORAL),
        ('GRID', (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(legend_tbl)
    story.append(Spacer(1, 3*mm))

    star_legend_s = ParagraphStyle('sl', fontName='Helvetica', fontSize=9,
        leading=13, textColor=GRAY, alignment=TA_CENTER)
    story.append(Paragraph(
        '<font color="#D4A017">\u2605\u2605\u2605\u2605\u2605</font> = Asked Almost Every Interview'
        '&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;'
        '<font color="#D4A017">\u2605\u2605\u2605</font><font color="#D6D0C0">\u2605\u2605</font> = Commonly Asked'
        '&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;'
        '<font color="#D4A017">\u2605</font><font color="#D6D0C0">\u2605\u2605\u2605\u2605</font> = Rarely Asked',
        star_legend_s))

    story.append(Spacer(1, 10*mm))

    # Phase grid
    phases = [
        ("Phase 1", "JavaScript &\nTypeScript"),
        ("Phase 2", "React &\nNext.js"),
        ("Phase 3", "Node.js &\nExpress"),
        ("Phase 4", "MongoDB &\nPostgreSQL"),
        ("Phase 5", "System Design\n& DSA"),
        ("Phase 6", "Architecture\n& DevOps"),
        ("Phase 7", "Testing &\nQA"),
        ("Phase 8", "API Design\n& GraphQL"),
    ]
    colors_list = [BLUE, GREEN, PURPLE, AMBER, CORAL, PINK, TEAL, OLIVE]
    bg_list = [LBLUE, LGREEN, LPURPLE, LAMBER, LCORAL, LPINK, LTEAL, LOLIVE]

    cw = (W - 40*mm) / 4
    for row_idx in range(0, len(phases), 4):
        row_data = []
        row_colors = []
        for j in range(4):
            if row_idx + j < len(phases):
                ph, name = phases[row_idx + j]
                c = colors_list[row_idx + j]
                bg = bg_list[row_idx + j]
                ph_s = ParagraphStyle('ph', fontName='Helvetica-Bold', fontSize=10,
                    leading=13, textColor=c, alignment=TA_CENTER)
                nm_s = ParagraphStyle('nm', fontName='Helvetica', fontSize=9,
                    leading=12, textColor=DGRAY, alignment=TA_CENTER)
                cell = [Paragraph(ph, ph_s), Paragraph(name, nm_s)]
                row_data.append(cell)
                row_colors.append(bg)
            else:
                row_data.append("")
                row_colors.append(WHITE)

        tbl = Table([row_data], colWidths=[cw]*4, rowHeights=[22*mm])
        styles = [
            ('GRID', (0,0), (-1,-1), 0.5, BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]
        for col_idx, bg_col in enumerate(row_colors):
            styles.append(('BACKGROUND', (col_idx,0), (col_idx,-1), bg_col))

        tbl.setStyle(TableStyle(styles))
        story.append(tbl)
        story.append(Spacer(1, 2*mm))

    story.append(PageBreak())

def build_phase_header(story, phase_name, q_count, bg):
    ph_s = ParagraphStyle('ph', fontName='Helvetica-Bold', fontSize=16,
        leading=20, textColor=WHITE)
    qc_s = ParagraphStyle('qc', fontName='Helvetica', fontSize=10,
        leading=13, textColor=colors.HexColor('#CECBF6'), alignment=TA_CENTER)

    data = [[
        Paragraph(phase_name, ph_s),
        Paragraph(f"{q_count} Q&amp;As", qc_s),
    ]]
    tbl = Table(data, colWidths=[W - 60*mm - 30*mm, 30*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (0,-1), 14),
        ('RIGHTPADDING', (-1,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(KeepTogether([tbl]))
    story.append(Spacer(1, 5*mm))

def build_question(story, q_num, level, rating, question, answer, code, tip):
    level_cfg = {
        'BASIC':        (colors.HexColor('#3B6D11'), colors.HexColor('#EAF3DE')),
        'INTERMEDIATE': (colors.HexColor('#185FA5'), colors.HexColor('#E6F1FB')),
        'ADVANCED':     (colors.HexColor('#993C1D'), colors.HexColor('#FAECE7')),
    }
    lc, lbg = level_cfg.get(level, (GRAY, LGRAY))

    num_s = ParagraphStyle('qn', fontName='Helvetica-Bold', fontSize=11,
        leading=14, textColor=NAVY)
    lvl_s = ParagraphStyle('lv', fontName='Helvetica-Bold', fontSize=8,
        leading=10, textColor=lc, alignment=TA_CENTER)
    star_s = ParagraphStyle('st', fontName='Helvetica', fontSize=10,
        leading=12, textColor=GOLD, alignment=TA_CENTER)

    star_html = stars_text(rating)

    header = Table(
        [[Paragraph(f"Q{q_num}", num_s),
          Paragraph(star_html, star_s),
          Paragraph(level, lvl_s)]],
        colWidths=[W - 60*mm - 50*mm, 24*mm, 26*mm]
    )
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), lbg),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (0,-1), 10),
        ('RIGHTPADDING', (-1,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    q_s = ParagraphStyle('qs', fontName='Helvetica-Bold', fontSize=11,
        leading=15, textColor=DGRAY, spaceBefore=3, spaceAfter=3)
    al_s = ParagraphStyle('al', fontName='Helvetica-Bold', fontSize=9,
        leading=11, textColor=GREEN, spaceBefore=4, spaceAfter=2)
    a_s  = ParagraphStyle('as', fontName='Helvetica', fontSize=10,
        leading=15, textColor=GRAY, alignment=TA_JUSTIFY)
    tip_s = ParagraphStyle('tp', fontName='Helvetica-Oblique', fontSize=9,
        leading=13, textColor=AMBER, leftIndent=6, spaceBefore=2)
    code_s = ParagraphStyle('cd', fontName='Courier', fontSize=8,
        leading=11, textColor=CODE_FG, leftIndent=8,
        backColor=CODE_BG, borderPadding=(5,8,5,8), spaceBefore=3, spaceAfter=3)

    elems = [header, Spacer(1, 1*mm), Paragraph(question, q_s),
             Paragraph("Answer:", al_s), Paragraph(answer, a_s)]

    if code:
        lines = code.split('\n')
        code_text = '<br/>'.join(
            ln.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace(' ','&nbsp;')
            for ln in lines
        )
        elems.append(Paragraph(code_text, code_s))

    if tip:
        elems.append(Paragraph("Interview tip: " + tip, tip_s))

    elems.append(HRFlowable(width='100%', thickness=0.4,
        color=colors.HexColor('#D3D1C7'), spaceAfter=3))

    story.append(KeepTogether(elems[:5]))
    for e in elems[5:]:
        story.append(e)
    story.append(Spacer(1, 2*mm))

enc = StandardEncryption("", "ninazmul_owner_password", canPrint=1, canModify=0, canCopy=1, canAnnotate=0)
doc = SimpleDocTemplate(
    "FullStack_Interview_QnA.pdf",
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=16*mm, bottomMargin=22*mm,
    title="Full-Stack Developer Interview Q&A — MERN & Next.js",
    author="Interview Prep Guide",
    subject="Full-Stack Developer Interview Preparation — All Levels",
    encrypt=enc,
)

story = []
build_cover(story)

q_num = 1
for phase_idx, (phase_name, questions) in enumerate(QNA.items()):
    bg, lbg = PHASE_COLORS[phase_idx]
    if phase_idx > 0:
        story.append(PageBreak())

    build_phase_header(story, phase_name, len(questions), bg)

    for level, rating, question, answer, code, tip in questions:
        build_question(story, q_num, level, rating, question, answer, code, tip)
        q_num += 1

doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
print(f"Done! Generated {q_num-1} questions across {len(QNA)} phases.")

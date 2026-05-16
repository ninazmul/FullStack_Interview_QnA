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
GRAY    = colors.HexColor('#444441')
LGRAY   = colors.HexColor('#F1EFE8')
DGRAY   = colors.HexColor('#2C2C2A')
CODE_BG = colors.HexColor('#F1EFE8')
CODE_FG = colors.HexColor('#26215C')
WHITE   = colors.white
BORDER  = colors.HexColor('#B5D4F4')

PHASE_COLORS = [
    (BLUE,   LBLUE),
    (GREEN,  LGREEN),
    (PURPLE, LPURPLE),
    (AMBER,  LAMBER),
    (CORAL,  LCORAL),
    (PINK,   LPINK),
    (TEAL,   LTEAL),
]

QNA = {
    "Phase 1: JavaScript & TypeScript Fundamentals": [
        ("BASIC","What is the difference between var, let, and const?",
         "var is function-scoped and hoisted (initialized to undefined). let and const are block-scoped and live in the Temporal Dead Zone until declared. const cannot be reassigned, but its object/array contents can still be mutated.",
         "var x = 1;\nif (true) {\n  var x = 10;  // same variable — function-scoped\n  let y = 20;  // block-scoped, dies here\n}\nconsole.log(x); // 10\n// console.log(y); // ReferenceError",
         "Prefer const by default; use let when reassignment is needed; avoid var in modern code."),

        ("BASIC","What is hoisting in JavaScript?",
         "Hoisting moves variable and function declarations to the top of their scope before execution. var is hoisted and initialized to undefined. Function declarations are fully hoisted. let and const are hoisted but stay in the Temporal Dead Zone (TDZ) — accessing them before declaration throws a ReferenceError.",
         "console.log(a); // undefined (var hoisted)\nvar a = 5;\n\ngreet(); // works — function fully hoisted\nfunction greet() { return 'hello'; }\n\nconsole.log(b); // ReferenceError (TDZ)\nlet b = 10;",
         "The TDZ is the gap between entering scope and the actual declaration line."),

        ("BASIC","Explain JavaScript closures with an example.",
         "A closure is a function that retains access to its outer scope even after that outer function has finished executing. Closures enable data encapsulation, factory functions, and stateful logic.",
         "function makeCounter() {\n  let count = 0;\n  return {\n    increment: () => ++count,\n    decrement: () => --count,\n    value: () => count,\n  };\n}\nconst c = makeCounter();\nc.increment(); c.increment();\nconsole.log(c.value()); // 2",
         "Each call to makeCounter() creates an independent closure with its own count."),

        ("BASIC","What is the difference between == and ===?",
         "== (loose equality) coerces types before comparing. === (strict equality) compares value AND type with no coercion. Always use === in production code to avoid subtle type-coercion bugs.",
         "0 == false      // true  (coercion)\n0 === false     // false (different types)\nnull == undefined  // true\nnull === undefined // false\n'' == 0         // true\n'' === 0        // false",
         "Use === everywhere. The only valid use of == is null-check: x == null catches both null and undefined."),

        ("BASIC","What are JavaScript primitive types?",
         "Primitives: string, number, bigint, boolean, undefined, null, symbol. Reference type: object (arrays, functions, maps, sets). Primitives are copied by value; objects are copied by reference.",
         "typeof 'hi'        // 'string'\ntypeof 42          // 'number'\ntypeof true        // 'boolean'\ntypeof undefined   // 'undefined'\ntypeof null        // 'object' (JS bug)\ntypeof []          // 'object'\ntypeof function(){} // 'function'",
         "typeof null === 'object' is a historical JavaScript bug — use null === x to check for null."),

        ("BASIC","What is the difference between null and undefined?",
         "undefined means a variable has been declared but not assigned a value — it's the default empty value. null is an intentional assignment meaning 'no value'. typeof undefined is 'undefined'; typeof null is 'object' (historical bug).",
         "let a;             // undefined automatically\nlet b = null;      // intentional empty\n\nfunction getUser(id) {\n  if (!id) return null; // intentional: no user\n}\n\nconsole.log(a == b);  // true (loose)\nconsole.log(a === b); // false (strict)",
         "Use null when you intentionally want to represent 'no value'. Let undefined arise naturally."),

        ("INTERMEDIATE","Explain the JavaScript event loop.",
         "JavaScript is single-threaded. The event loop manages async operations via the call stack, Web APIs, microtask queue, and callback (macro-task) queue. Microtasks (Promises, queueMicrotask) always run before macrotasks (setTimeout, setInterval) — the microtask queue is fully drained after each task.",
         "console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');\n// Output: 1, 4, 3, 2\n// Microtask (3) runs before macrotask (2)",
         "setTimeout(fn, 0) does not mean immediate — it means 'run after current + microtasks finish'."),

        ("INTERMEDIATE","What is the difference between Promise, async/await, and callbacks?",
         "Callbacks lead to callback hell when nested. Promises provide cleaner chaining with .then()/.catch(). async/await is syntactic sugar over Promises — makes async code read synchronously, easier to debug and reason about.",
         "// Callback hell\nfetchUser(id, (err, user) => {\n  fetchPosts(user.id, (err, posts) => {\n    fetchComments(posts[0].id, (err, comments) => {});\n  });\n});\n\n// async/await (clean)\nasync function load(id) {\n  try {\n    const user = await fetchUser(id);\n    const posts = await fetchPosts(user.id);\n    const comments = await fetchComments(posts[0].id);\n  } catch(e) { console.error(e); }\n}",
         "Always handle rejections. Unhandled promise rejections crash Node.js processes."),

        ("INTERMEDIATE","Explain prototypal inheritance in JavaScript.",
         "Every JS object has an internal [[Prototype]] link. When accessing a property, JS walks the prototype chain until it finds it or reaches null. ES6 classes are syntactic sugar over this mechanism.",
         "function Animal(name) { this.name = name; }\nAnimal.prototype.speak = function() {\n  return this.name + ' speaks';\n};\n\nconst dog = new Animal('Rex');\nconsole.log(dog.speak()); // Rex speaks\nconsole.log(dog.__proto__ === Animal.prototype); // true\nconsole.log(dog.hasOwnProperty('speak')); // false",
         "hasOwnProperty distinguishes own properties from inherited prototype properties."),

        ("INTERMEDIATE","Explain the classic var + closure loop problem.",
         "With var in a for loop, all callbacks share the same variable reference. By execution time, i holds its final value. Fix: use let (block-scoped per iteration) or an IIFE to capture each value.",
         "// Problem — prints 3,3,3\nfor (var i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 0);\n}\n\n// Fix 1: let (block-scoped)\nfor (let i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 0); // 0,1,2\n}\n\n// Fix 2: IIFE\nfor (var i = 0; i < 3; i++) {\n  ((j) => setTimeout(() => console.log(j), 0))(i);\n}",
         "This is one of the most common closure interview questions — know both fixes."),

        ("INTERMEDIATE","What is the difference between call, apply, and bind?",
         "All three set the this context. call() invokes immediately with args as a list. apply() invokes immediately with args as array. bind() returns a new function with this permanently bound — useful for event handlers and partial application.",
         "function greet(greeting, punct) {\n  return greeting + ', ' + this.name + punct;\n}\nconst user = { name: 'Nazmul' };\n\ngreet.call(user, 'Hello', '!');   // 'Hello, Nazmul!'\ngreet.apply(user, ['Hi', '?']);   // 'Hi, Nazmul?'\nconst fn = greet.bind(user, 'Hey');\nfn('.');  // 'Hey, Nazmul.'",
         "bind is commonly used to preserve this in class methods passed as React event handlers."),

        ("INTERMEDIATE","What are Promise.all, Promise.race, Promise.allSettled, and Promise.any?",
         "Promise.all: resolves when all resolve; rejects if any reject. Promise.race: resolves/rejects as soon as first settles. Promise.allSettled: waits for all — never rejects, returns status of each. Promise.any: resolves with first success; rejects only if all fail.",
         "const p1 = fetch('/api/users');\nconst p2 = fetch('/api/posts');\n\n// All must succeed\nconst [users, posts] = await Promise.all([p1, p2]);\n\n// Results regardless of failure\nconst results = await Promise.allSettled([p1, p2]);\nresults.forEach(r => {\n  if (r.status === 'fulfilled') console.log(r.value);\n  else console.log(r.reason);\n});",
         "Use Promise.allSettled when you need results from all — even failed — promises."),

        ("INTERMEDIATE","What are arrow functions and how do they differ from regular functions?",
         "Arrow functions are concise, don't have their own this (inherit from enclosing scope), no arguments object, cannot be used as constructors, and don't have a prototype property. Perfect for callbacks and array methods.",
         "// Regular function — has own 'this'\nfunction Timer() {\n  this.count = 0;\n  setInterval(function() {\n    this.count++; // 'this' is undefined in strict\n  }, 1000);\n}\n\n// Arrow function — inherits 'this'\nfunction Timer() {\n  this.count = 0;\n  setInterval(() => {\n    this.count++; // 'this' is Timer instance\n  }, 1000);\n}",
         "Never use arrow functions as object methods if you need this to refer to the object."),

        ("ADVANCED","What are WeakMap and WeakSet? When would you use them?",
         "WeakMap and WeakSet hold weak references — they don't prevent garbage collection of keys/values. Keys must be objects. Neither is iterable. Used for: attaching private metadata to objects, caching without memory leaks, tracking presence without preventing GC.",
         "const cache = new WeakMap();\n\nfunction process(obj) {\n  if (cache.has(obj)) return cache.get(obj);\n  const result = heavyComputation(obj);\n  cache.set(obj, result); // auto-removed when obj is GC'd\n  return result;\n}\n\n// Regular Map would prevent GC of obj\n// WeakMap allows GC — no memory leak",
         "WeakMap is the correct tool for associating data with DOM nodes without memory leaks."),

        ("ADVANCED","Explain TypeScript generics.",
         "Generics write reusable, type-safe code that works with multiple types. Instead of any (loses type info), generics capture the type at call time and propagate it through the function or class.",
         "function identity<T>(arg: T): T { return arg; }\n\n// Real-world: typed API response\nasync function fetchData<T>(url: string): Promise<T> {\n  const res = await fetch(url);\n  return res.json() as T;\n}\n\ninterface User { id: number; name: string; }\nconst user = await fetchData<User>('/api/user/1');\nuser.name; // TypeScript knows this is string",
         "Use constraints (T extends object) to limit which types can be passed."),

        ("ADVANCED","What are TypeScript utility types?",
         "Utility types transform existing types. Partial<T> makes all optional. Required<T> makes all mandatory. Pick<T,K> selects keys. Omit<T,K> removes keys. Record<K,V> maps key to value type. Readonly<T> prevents mutation.",
         "interface User {\n  id: number; name: string;\n  email: string; age: number;\n}\n\ntype UpdateUser = Partial<User>;\n// All fields optional — for PATCH requests\n\ntype UserPreview = Pick<User, 'id' | 'name'>;\n// Only id and name\n\ntype PublicUser = Omit<User, 'email'>;\n// Everything except email\n\ntype UserMap = Record<string, User>;\n// { [key: string]: User }",
         "Combine utility types: Partial<Pick<User, 'name' | 'email'>> for partial update DTOs."),

        ("ADVANCED","What is the difference between interface and type in TypeScript?",
         "Both define shapes. Interfaces support extends and declaration merging (same interface declared twice merges). Types are more flexible — can represent unions, intersections, tuples, and primitives. Interfaces for object shapes; types for unions and complex compositions.",
         "interface Animal { name: string; }\ninterface Dog extends Animal { breed: string; }\n\n// Declaration merging (interfaces only)\ninterface Window { myProp: string; }\ninterface Window { another: number; } // merged\n\n// Types handle unions\ntype ID = string | number;\ntype Result<T> = { data: T } | { error: string };\ntype Point = [number, number]; // tuple",
         "In a codebase, pick one and be consistent. Most teams use interface for objects, type for the rest."),

        ("ADVANCED","Explain JavaScript memory management and memory leak patterns.",
         "JS uses mark-and-sweep garbage collection. Memory leaks occur when references are unintentionally kept alive. Common causes: forgotten event listeners, closures holding large objects, global variables, detached DOM nodes in variables, and uncleaned setInterval.",
         "// LEAK: listener never removed\nfunction setup() {\n  const bigData = new Array(1e6).fill('x');\n  document.addEventListener('click', () => {\n    console.log(bigData.length); // bigData never GC'd\n  });\n}\n\n// FIX: remove listener\nconst handler = () => console.log('clicked');\ndocument.addEventListener('click', handler);\n// Cleanup:\ndocument.removeEventListener('click', handler);",
         "Use Chrome DevTools Memory tab and heap snapshots to identify leaks in production."),

        ("ADVANCED","What is the JavaScript Proxy object?",
         "Proxy wraps an object and intercepts fundamental operations (get, set, delete, apply). Reflect provides the same operations as static methods. Together they enable reactive systems, validation, logging — Vue 3's reactivity is built on Proxy.",
         "const handler = {\n  get(target, key) {\n    console.log('Getting: ' + key);\n    return Reflect.get(target, key);\n  },\n  set(target, key, value) {\n    if (typeof value !== 'number')\n      throw new TypeError('Must be number');\n    return Reflect.set(target, key, value);\n  }\n};\nconst state = new Proxy({}, handler);\nstate.count = 5;  // validated\nstate.count;      // logs 'Getting: count'",
         "Proxy is how Vue 3 implements reactivity — understanding it is a strong senior signal."),

        ("ADVANCED","What is the difference between shallow copy and deep copy?",
         "Shallow copy duplicates the top level but nested objects share references. Deep copy recursively duplicates everything — fully independent. Object spread and Object.assign are shallow. structuredClone() is the modern native deep copy.",
         "const orig = { a: 1, b: { c: 2 } };\n\n// Shallow — b is shared\nconst shallow = { ...orig };\nshallow.b.c = 99;\nconsole.log(orig.b.c); // 99 (mutated!)\n\n// Deep — fully independent\nconst deep = structuredClone(orig);\ndeep.b.c = 99;\nconsole.log(orig.b.c); // 2 (safe)",
         "JSON.parse(JSON.stringify()) fails on Date, undefined, functions, and circular refs — use structuredClone."),

        ("ADVANCED","Explain JavaScript generators.",
         "Generator functions (function*) produce iterators via yield. They enable lazy evaluation, infinite sequences, and custom iteration. When you call next(), execution runs until the next yield and pauses.",
         "function* range(start, end, step = 1) {\n  for (let i = start; i < end; i += step) yield i;\n}\nfor (const n of range(0, 10, 2)) {\n  console.log(n); // 0, 2, 4, 6, 8\n}\n\nfunction* fibonacci() {\n  let [a, b] = [0, 1];\n  while (true) { yield a; [a,b] = [b, a+b]; }\n}\nconst fib = fibonacci();\nfib.next().value; // 0\nfib.next().value; // 1",
         "Generators power async iteration (for await...of) and are the foundation of Redux-Saga."),
    ],

    "Phase 2: React & Next.js": [
        ("BASIC","What is the Virtual DOM?",
         "The Virtual DOM is a lightweight JS representation of the real DOM. React creates a new virtual tree on state change, diffs it with the previous one (reconciliation), and updates only changed nodes in the real DOM — minimizing expensive DOM operations.",
         "// React handles diffing automatically:\nfunction Counter() {\n  const [n, setN] = useState(0);\n  return (\n    <button onClick={() => setN(c => c+1)}>\n      Count: {n}\n    </button>\n  );\n  // Only the text node updates, not the whole button",
         "React's diffing algorithm assumes same-type elements at the same position are the same component."),

        ("BASIC","What is the difference between controlled and uncontrolled components?",
         "Controlled: form data is driven by React state — every change fires onChange and updates state. Uncontrolled: data lives in the DOM, accessed via refs. Controlled is preferred for validation and conditional logic.",
         "// Controlled\nfunction Controlled() {\n  const [val, setVal] = useState('');\n  return (\n    <input\n      value={val}\n      onChange={e => setVal(e.target.value)}\n    />\n  );\n}\n\n// Uncontrolled\nfunction Uncontrolled() {\n  const ref = useRef();\n  const submit = () => console.log(ref.current.value);\n  return <input ref={ref} />;\n}",
         "File inputs are always uncontrolled — their value is read-only in the DOM."),

        ("BASIC","What is the difference between useEffect and useLayoutEffect?",
         "useEffect runs asynchronously after the browser paints. useLayoutEffect runs synchronously after DOM mutations but before paint. Use useLayoutEffect when you need to read/mutate layout (measure size, avoid visual flicker). Prefer useEffect by default.",
         "// useEffect — after paint (async, no flicker risk)\nuseEffect(() => {\n  document.title = 'Updated: ' + count;\n}, [count]);\n\n// useLayoutEffect — before paint (sync)\nuseLayoutEffect(() => {\n  const { height } = ref.current.getBoundingClientRect();\n  setHeight(height); // set before user sees anything\n}, []);",
         "Only reach for useLayoutEffect when you see visual flickering with useEffect."),

        ("INTERMEDIATE","Explain useMemo and useCallback — when to use them.",
         "useMemo memoizes a computed value. useCallback memoizes a function reference. Both only re-compute/re-create when dependencies change. Use them to prevent child re-renders or avoid expensive recalculations. Do not use prematurely — measure first.",
         "// useMemo — skip re-sorting on unrelated renders\nconst sorted = useMemo(\n  () => [...items].sort((a,b) => a.price - b.price),\n  [items]\n);\n\n// useCallback — stable ref for memo'd child\nconst handleClick = useCallback(\n  () => dispatch({ type: 'INCREMENT' }),\n  [dispatch]\n);\n\n<ExpensiveChild onClick={handleClick} />",
         "useMemo/useCallback have overhead too. Add them only after profiling shows a real problem."),

        ("INTERMEDIATE","How does React Context API work? What are its limitations?",
         "Context passes data through the tree without prop drilling. Create context, wrap with Provider, consume with useContext. Limitation: any Provider value change re-renders ALL consumers — even those not using the changed value. For high-frequency state, use Zustand or Redux instead.",
         "const ThemeCtx = createContext('light');\n\nfunction App() {\n  const [theme, setTheme] = useState('light');\n  return (\n    <ThemeCtx.Provider value={{ theme, setTheme }}>\n      <Layout />\n    </ThemeCtx.Provider>\n  );\n}\n\nfunction Button() {\n  const { theme } = useContext(ThemeCtx);\n  return <button className={theme}>Click</button>;\n}",
         "Split context by concern — separate ThemeContext from UserContext to avoid unnecessary re-renders."),

        ("INTERMEDIATE","What role do keys play in React lists?",
         "Keys help React identify which items changed, were added, or removed during reconciliation. Bad keys (array index) cause bugs when items reorder or have local state. Always use stable, unique IDs.",
         "// Bad — using index as key\nitems.map((item, i) => <Item key={i} data={item} />);\n// If items reorder, React thinks content\n// changed in place — local state is wrong\n\n// Good — stable unique ID\nitems.map(item => (\n  <Item key={item.id} data={item} />\n));",
         "Keys must be stable across renders, unique among siblings, and not randomly generated at render time."),

        ("INTERMEDIATE","Explain Next.js rendering: SSR, SSG, ISR, CSR.",
         "SSR: HTML generated per request — real-time, personalized. SSG: HTML built at compile time — fastest, great for blogs/docs. ISR: SSG with timed revalidation — content stays fresh without full rebuilds. CSR: rendered in browser — used for dashboards behind auth.",
         "// SSG (force-cache = static)\nasync function Page() {\n  const data = await fetch(url, { cache: 'force-cache' });\n  return <Render data={data} />;\n}\n\n// ISR — revalidate every 60 seconds\nasync function Page() {\n  const data = await fetch(url, { next: { revalidate: 60 } });\n  return <Render data={data} />;\n}\n\n// SSR — always fresh\nasync function Page() {\n  const data = await fetch(url, { cache: 'no-store' });\n  return <Render data={data} />;\n}",
         "ISR is the default recommendation for most marketing and content pages."),

        ("INTERMEDIATE","What is the difference between Server Components and Client Components?",
         "Server Components (default in App Router) render on the server, can access databases directly, have no client JS cost, but cannot use hooks or browser APIs. Client Components ('use client') run in the browser, support hooks and events, but add to the JS bundle.",
         "'use client';\nimport { useState } from 'react';\n\n// Client Component\nexport function Counter() {\n  const [n, setN] = useState(0);\n  return <button onClick={() => setN(n+1)}>{n}</button>;\n}\n\n// Server Component (no directive)\nasync function UserList() {\n  const users = await db.user.findMany();\n  return users.map(u => <li key={u.id}>{u.name}</li>);\n}",
         "Server Components reduce JS bundle size. Push 'use client' as far down the tree as possible."),

        ("INTERMEDIATE","How do you prevent unnecessary re-renders?",
         "1) React.memo — skip re-render if props haven't changed. 2) useCallback — stable function refs. 3) useMemo — memoize derived values. 4) State colocation — keep state close to where it's used. 5) Context splitting — separate fast-changing from slow-changing context. 6) Virtualize long lists.",
         "// React.memo\nconst Card = React.memo(({ user }) => (\n  <div>{user.name}</div>\n));\n\n// Colocate state — don't lift unnecessarily\nfunction Form() {\n  // This state only affects Form\n  const [value, setValue] = useState('');\n  return <input value={value} onChange={e => setValue(e.target.value)} />;\n}",
         "Use React DevTools Profiler to identify what's actually re-rendering before optimizing."),

        ("INTERMEDIATE","Explain useReducer and when to prefer it over useState.",
         "useReducer manages complex state via a pure reducer function. Prefer it when: state has multiple interrelated sub-values, transitions are complex, or you want testable state logic separate from components.",
         "type Action =\n  | { type: 'INCREMENT' }\n  | { type: 'DECREMENT' }\n  | { type: 'RESET' };\n\nfunction reducer(state: number, action: Action) {\n  switch (action.type) {\n    case 'INCREMENT': return state + 1;\n    case 'DECREMENT': return state - 1;\n    case 'RESET': return 0;\n    default: return state;\n  }\n}\n\nconst [count, dispatch] = useReducer(reducer, 0);\ndispatch({ type: 'INCREMENT' });",
         "useReducer + Context is a lightweight alternative to Redux for medium complexity."),

        ("ADVANCED","Explain Next.js Middleware and its use cases.",
         "Middleware runs on the Edge before requests complete — can redirect, rewrite URLs, set headers, check auth. Runs before page rendering with near-zero latency because it executes at CDN edge nodes globally.",
         "// middleware.ts\nimport { NextResponse } from 'next/server';\nimport type { NextRequest } from 'next/server';\n\nexport function middleware(req: NextRequest) {\n  const token = req.cookies.get('token');\n  if (!token &&\n    req.nextUrl.pathname.startsWith('/dashboard')) {\n    return NextResponse.redirect(\n      new URL('/login', req.url)\n    );\n  }\n  return NextResponse.next();\n}\n\nexport const config = {\n  matcher: ['/dashboard/:path*'],\n};",
         "Middleware is ideal for auth guards, A/B testing, geolocation-based routing, and i18n redirects."),

        ("ADVANCED","How do you implement code splitting in Next.js?",
         "Next.js automatically splits by page. Dynamic imports with next/dynamic enable component-level splitting for heavy components like charts, editors, or map libraries. Use ssr: false for browser-only components.",
         "import dynamic from 'next/dynamic';\n\n// Heavy chart only loaded when rendered\nconst Chart = dynamic(\n  () => import('../components/Chart'),\n  {\n    loading: () => <p>Loading chart...</p>,\n    ssr: false, // browser-only component\n  }\n);\n\nexport default function Dashboard() {\n  return (\n    <main>\n      <h1>Dashboard</h1>\n      <Chart data={data} />\n    </main>\n  );\n}",
         "Use ssr: false for components using window, document, or other browser-only APIs."),

        ("ADVANCED","How would you implement authentication in Next.js?",
         "Best practice: use Auth.js (NextAuth). For custom: store JWT in httpOnly cookies (not localStorage — XSS-safe). Use Middleware to protect routes. Server Components read cookies directly; Client Components use a session hook.",
         "// Route handler — login\nexport async function POST(req: Request) {\n  const { email, password } = await req.json();\n  const user = await validateUser(email, password);\n  if (!user)\n    return Response.json({ error: 'Unauthorized' }, { status: 401 });\n\n  const token = signJWT({ id: user.id, role: user.role });\n  const res = Response.json({ ok: true });\n  res.headers.set('Set-Cookie',\n    `token=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=3600`\n  );\n  return res;\n}",
         "Never store JWTs in localStorage — they are vulnerable to XSS attacks. Always use httpOnly cookies."),

        ("ADVANCED","What are Web Vitals (LCP, CLS, INP) and why are they important in Next.js?",
         "Core Web Vitals are Google's metrics for measuring user experience. LCP (Largest Contentful Paint) measures loading performance (aim < 2.5s). CLS (Cumulative Layout Shift) measures visual stability (aim < 0.1). INP (Interaction to Next Paint) measures interactivity/responsiveness (aim < 200ms). They heavily impact SEO.",
         "import { useReportWebVitals } from 'next/web-vitals'\n\nexport function WebVitals() {\n  useReportWebVitals((metric) => {\n    if (metric.name === 'LCP') {\n      console.log('LCP:', metric.value);\n      // Send to analytics\n    }\n  })\n}",
         "Next.js optimizes these automatically via next/image (CLS/LCP), next/font (CLS), and Server Components (INP)."),
    ],

    "Phase 3: Node.js & Express": [
        ("BASIC","How does Node.js handle async if it is single-threaded?",
         "Node.js delegates async operations (file I/O, network, timers) to libuv's thread pool and the OS. The single-threaded event loop continuously checks for completed operations and runs callbacks. This allows handling thousands of concurrent connections without threads.",
         "const fs = require('fs');\n\n// Non-blocking — delegates to OS\nfs.readFile('large.txt', 'utf8', (err, data) => {\n  // Runs when I/O completes\n  console.log('Done:', data.length);\n});\n\nconsole.log('Runs first — sync'); // runs immediately",
         "CPU-bound tasks block the event loop — use worker_threads or child_process for those."),

        ("BASIC","What is Express middleware and how does it work?",
         "Middleware are functions with access to req, res, and next(). They form a pipeline — each can process the request and pass it forward via next(). Order matters. Types: application-level, router-level, error-handling (4 params), built-in, and third-party.",
         "const app = express();\n\n// Logger middleware\napp.use((req, res, next) => {\n  console.log(req.method + ' ' + req.path);\n  next();\n});\n\n// Auth middleware\napp.use('/api', requireAuth);\n\n// Error handler (4 params — must be last)\napp.use((err, req, res, next) => {\n  res.status(500).json({ error: err.message });\n});",
         "Error-handling middleware MUST have exactly 4 parameters (err, req, res, next) to work."),

        ("INTERMEDIATE","How do you structure a large Node.js application?",
         "Layered architecture: Routes (HTTP layer) -> Controllers (req/res handling) -> Services (business logic) -> Repositories/Models (data access). This separation makes code testable, maintainable, and scalable.",
         "// routes/user.routes.ts\nrouter.post('/users',\n  validate(createUserSchema),\n  userController.create\n);\n\n// controllers/user.controller.ts\nasync create(req, res, next) {\n  try {\n    const user = await userService.create(req.body);\n    res.status(201).json(user);\n  } catch(e) { next(e); }\n}\n\n// services/user.service.ts\nasync create(data) {\n  await this.verifyEmailUnique(data.email);\n  return userRepository.save(data);\n}",
         "Never put business logic in controllers or routes — it kills testability."),

        ("INTERMEDIATE","Explain JWT authentication flow.",
         "1) User submits credentials. 2) Server validates and signs a JWT with secret. 3) Client stores token and sends it in Authorization header. 4) Server verifies token on protected routes. 5) Short-lived access token (15min); long-lived refresh token in httpOnly cookie.",
         "// Sign on login\nconst token = jwt.sign(\n  { userId: user.id, role: user.role },\n  process.env.JWT_SECRET,\n  { expiresIn: '15m' }\n);\n\n// Verify middleware\nfunction authenticate(req, res, next) {\n  const token = req.headers.authorization?.split(' ')[1];\n  if (!token) return res.status(401).json({ error: 'No token' });\n  try {\n    req.user = jwt.verify(token, process.env.JWT_SECRET);\n    next();\n  } catch { res.status(401).json({ error: 'Invalid token' }); }\n}",
         "Access token: 15 min in memory/header. Refresh token: 7-30 days in httpOnly cookie."),

        ("INTERMEDIATE","What is RBAC and how do you implement it in Express?",
         "Role-Based Access Control restricts routes based on user roles. Each role has a set of permissions. Middleware checks the user's role before granting access. Decouples access logic from business logic.",
         "const permissions = {\n  admin:  ['read','write','delete'],\n  editor: ['read','write'],\n  viewer: ['read'],\n};\n\nfunction authorize(...perms) {\n  return (req, res, next) => {\n    const userPerms = permissions[req.user.role] || [];\n    const allowed = perms.every(p => userPerms.includes(p));\n    if (!allowed)\n      return res.status(403).json({ error: 'Forbidden' });\n    next();\n  };\n}\n\nrouter.delete('/posts/:id',\n  authenticate,\n  authorize('delete'),\n  postController.delete\n);",
         "For complex permission systems, consider Casbin or OPA (Open Policy Agent)."),

        ("INTERMEDIATE","How do you handle errors globally in Express?",
         "Use a centralized error handler as the last middleware. Wrap async handlers with a utility to catch promise rejections. Define custom error classes for HTTP statuses. Never send stack traces to clients in production.",
         "// Custom error class\nclass AppError extends Error {\n  constructor(message, statusCode) {\n    super(message);\n    this.statusCode = statusCode;\n  }\n}\n\n// Async wrapper — catches promise rejections\nconst catchAsync = fn =>\n  (req, res, next) =>\n    Promise.resolve(fn(req, res, next)).catch(next);\n\n// Global handler\napp.use((err, req, res, next) => {\n  const status = err.statusCode || 500;\n  res.status(status).json({\n    error: err.message,\n    ...(process.env.NODE_ENV !== 'production'\n      && { stack: err.stack })\n  });\n});",
         "Express only catches sync errors automatically — always handle async with catchAsync or try/catch."),

        ("ADVANCED","How do you implement rate limiting in a distributed Node.js system?",
         "express-rate-limit handles single-server limits. For distributed systems (multiple servers), use Redis as a shared store so rate limits apply across all instances consistently.",
         "const rateLimit = require('express-rate-limit');\nconst RedisStore = require('rate-limit-redis');\n\nconst limiter = rateLimit({\n  windowMs: 15 * 60 * 1000, // 15 minutes\n  max: 100,\n  standardHeaders: true,\n  store: new RedisStore({\n    client: redisClient,\n    prefix: 'rl:',\n  }),\n  keyGenerator: req => req.user?.id || req.ip,\n});\n\n// Stricter limit on auth routes\nconst authLimiter = rateLimit({\n  windowMs: 60 * 1000,\n  max: 5, // 5 attempts per minute\n});\n\napp.use('/api/', limiter);\napp.use('/api/auth/', authLimiter);",
         "Apply stricter limits on /login and /register to prevent brute-force attacks."),

        ("ADVANCED","Explain Node.js streams and when to use them.",
         "Streams process data in chunks rather than loading everything into memory. Types: Readable, Writable, Duplex, Transform. Critical for large file handling, video streaming, and data pipelines — prevents memory overflow.",
         "const fs = require('fs');\nconst zlib = require('zlib');\n\n// Stream large file through gzip compression\n// Without streams: entire file in RAM\n// With streams: chunk by chunk\nfs.createReadStream('large.csv')\n  .pipe(zlib.createGzip())\n  .pipe(fs.createWriteStream('large.csv.gz'))\n  .on('finish', () => console.log('Compressed'));\n\n// Stream DB query results to HTTP response\napp.get('/export', (req, res) => {\n  res.setHeader('Content-Type', 'text/csv');\n  db.queryStream('SELECT * FROM orders')\n    .pipe(csvTransform)\n    .pipe(res);\n});",
         "Never use fs.readFile for large files — always stream them."),

        ("ADVANCED","How do you implement WebSockets for real-time features?",
         "WebSockets provide full-duplex persistent connections — ideal for chat, live updates, collaborative tools. HTTP polling wastes bandwidth; WebSockets push instantly. Use Socket.IO for production. Scale across multiple servers with Redis pub/sub adapter.",
         "const { Server } = require('socket.io');\nconst io = new Server(httpServer);\n\nio.on('connection', socket => {\n  socket.on('join-room', roomId => {\n    socket.join(roomId);\n    socket.to(roomId).emit('user-joined', socket.id);\n  });\n\n  socket.on('message', ({ roomId, text }) => {\n    io.to(roomId).emit('message', {\n      from: socket.id,\n      text,\n      at: new Date().toISOString()\n    });\n  });\n\n  socket.on('disconnect', () => {\n    console.log('Disconnected:', socket.id);\n  });\n});",
         "Use @socket.io/redis-adapter to sync events across multiple Node.js instances."),
    ],

    "Phase 4: MongoDB & PostgreSQL": [
        ("BASIC","When should you use MongoDB vs PostgreSQL?",
         "MongoDB excels with flexible documents, nested/hierarchical data, rapidly evolving schemas, and horizontal scale. PostgreSQL excels with relational data, complex joins, ACID transactions, and strong consistency requirements. Many production apps use both.",
         "// MongoDB — flexible nested document\n{\n  _id: '123',\n  name: 'Nazmul',\n  addresses: [\n    { type: 'home', city: 'Dhaka' },\n    { type: 'work', city: 'Mirpur' }\n  ]\n}\n\n// PostgreSQL — normalized\n-- users: id, name\n-- addresses: id, user_id FK, type, city",
         "Need ACID transactions and complex joins? PostgreSQL. Need schema flexibility and scale? MongoDB."),

        ("BASIC","What are database indexes and why do they matter?",
         "Indexes are data structures (typically B-trees) that allow the database to find rows without full table scans. Without an index on a WHERE column: O(n) scan. With an index: O(log n). Trade-off: indexes speed reads but slow writes and use storage.",
         "-- PostgreSQL\nCREATE INDEX idx_users_email ON users(email);\nCREATE INDEX idx_posts_user_created\n  ON posts(user_id, created_at DESC); -- composite\n\n-- MongoDB\ndb.users.createIndex({ email: 1 }, { unique: true });\ndb.orders.createIndex(\n  { userId: 1, createdAt: -1 }\n);",
         "Use EXPLAIN ANALYZE (Postgres) or .explain('executionStats') (MongoDB) to verify index usage."),

        ("INTERMEDIATE","Explain MongoDB's aggregation pipeline.",
         "The aggregation pipeline processes documents through sequential stages, each transforming output. Key stages: $match (filter early), $group (aggregate), $project (reshape), $sort, $limit, $lookup (join), $unwind (flatten arrays).",
         "db.orders.aggregate([\n  { $match: { status: 'completed' } },\n  { $group: {\n    _id: '$userId',\n    totalSpent: { $sum: '$amount' },\n    orderCount: { $sum: 1 }\n  }},\n  { $lookup: {\n    from: 'users',\n    localField: '_id',\n    foreignField: '_id',\n    as: 'user'\n  }},\n  { $unwind: '$user' },\n  { $sort: { totalSpent: -1 } },\n  { $limit: 10 }\n]);",
         "Always put $match as early as possible in the pipeline to reduce document count in later stages."),

        ("INTERMEDIATE","What are PostgreSQL transactions and ACID properties?",
         "ACID: Atomicity (all or nothing), Consistency (always valid state), Isolation (concurrent transactions don't interfere), Durability (committed data survives crashes). Transactions group operations so partial failures roll back entirely.",
         "BEGIN;\n\nUPDATE accounts\n  SET balance = balance - 500\n  WHERE id = 1;\n\nUPDATE accounts\n  SET balance = balance + 500\n  WHERE id = 2;\n\nCOMMIT; -- Both succeed or both roll back\n\n-- Savepoints for partial rollback\nSAVEPOINT before_step;\n-- ... more operations ...\nROLLBACK TO SAVEPOINT before_step;",
         "MongoDB 4.0+ supports multi-document ACID transactions, but they add overhead vs SQL."),

        ("INTERMEDIATE","What is the N+1 query problem and how do you solve it?",
         "N+1 occurs when you fetch N records then make 1 additional query per record. Example: 100 posts + 1 query per author = 101 queries. Fix: SQL JOINs / ORM eager loading, DataLoader batching, or MongoDB $lookup.",
         "// N+1 problem\nconst posts = await Post.findAll(); // 1 query\nfor (const post of posts) {\n  // N queries!\n  const author = await User.findById(post.userId);\n}\n\n// Fix: eager load (1 JOIN query)\nconst posts = await Post.findAll({\n  include: [{ model: User, as: 'author' }]\n});\n\n// MongoDB fix: $lookup\ndb.posts.aggregate([\n  { $lookup: {\n    from: 'users', localField: 'userId',\n    foreignField: '_id', as: 'author'\n  }}\n]);",
         "Enable query logging in development to detect N+1 — Mongoose debug mode, Sequelize logging: true."),

        ("ADVANCED","Explain read replicas and database sharding.",
         "Read Replicas: copies of primary DB for read traffic. Writes to primary, reads from replicas. Reduces read pressure. Sharding: partitions data across multiple DBs by shard key (range or hash). Each shard is independent. Enables horizontal scaling beyond single-machine limits.",
         "// Read/write separation\nawait primaryPool.query('INSERT INTO orders...');\nawait replicaPool.query('SELECT * FROM orders WHERE userId = $1', [id]);\n\n// MongoDB sharding\nsh.enableSharding('mydb');\nsh.shardCollection('mydb.users', { region: 'hashed' });\n// Asia users -> Shard A\n// Europe users -> Shard B\n// Queries route automatically",
         "Choose shard keys carefully — a bad key causes hot spots where one shard gets all the traffic."),

        ("ADVANCED","How do you optimize a slow SQL query?",
         "Steps: 1) EXPLAIN ANALYZE — see the query plan. 2) Check for missing indexes. 3) Avoid SELECT * — only fetch needed columns. 4) Avoid functions on indexed columns in WHERE. 5) Paginate large results. 6) Use covering indexes. 7) Consider query result caching with Redis.",
         "-- Slow: function prevents index use\nSELECT * FROM users\nWHERE LOWER(email) = 'test@example.com';\n\n-- Fix: index on expression\nCREATE INDEX idx_lower_email\n  ON users(LOWER(email));\n\n-- Better projection\nSELECT id, name, email FROM users\nWHERE LOWER(email) = 'test@example.com';\n\n-- Check plan\nEXPLAIN ANALYZE\nSELECT id, name FROM users\nWHERE email = 'x@y.com';",
         "'Seq Scan' in EXPLAIN output = no index used. 'Index Scan' = good. 'Bitmap Heap Scan' = ok."),

        ("ADVANCED","Explain MongoDB schema design: embedding vs referencing.",
         "Embed when: data always accessed together, bounded one-to-many, child data rarely changes alone. Reference when: many-to-many, data accessed independently, unbounded arrays, or documents risk exceeding 16MB.",
         "// Embed — post with few comments\n{\n  _id: 'post1',\n  title: 'Hello World',\n  comments: [\n    { author: 'Ali', text: 'Great!' }\n  ]\n}\n\n// Reference — user with millions of orders\n// users: { _id, name, email }\n// orders: { _id, userId: ObjectId, amount }\n\n// Query with $lookup\ndb.orders.aggregate([\n  { $lookup: {\n    from: 'users',\n    localField: 'userId',\n    foreignField: '_id',\n    as: 'user'\n  }}\n]);",
         "MongoDB documents have a hard 16MB limit — never embed unbounded arrays."),
    ],

    "Phase 5: System Design & DSA": [
        ("BASIC","What is Big O notation? Give examples.",
         "Big O describes time/space complexity as input size grows. O(1) constant, O(log n) binary search, O(n) linear, O(n log n) merge sort, O(n^2) nested loops, O(2^n) exponential.",
         "// O(1) — hash lookup\nconst map = new Map();\nmap.get('key'); // constant\n\n// O(n) — linear scan\narray.find(x => x === target);\n\n// O(log n) — binary search\nfunction binarySearch(arr, target) {\n  let lo = 0, hi = arr.length - 1;\n  while (lo <= hi) {\n    const mid = (lo + hi) >> 1;\n    if (arr[mid] === target) return mid;\n    arr[mid] < target ? lo = mid+1 : hi = mid-1;\n  }\n  return -1;\n}",
         "In interviews: state time complexity, then space complexity — both matter."),

        ("INTERMEDIATE","Two Sum problem — optimal approach.",
         "Naive: O(n^2) nested loops. Optimal: one pass with a hash map — O(n) time, O(n) space. For each number, check if its complement (target - num) already exists in the map. This pattern solves dozens of array problems.",
         "function twoSum(nums, target) {\n  const map = new Map(); // value -> index\n\n  for (let i = 0; i < nums.length; i++) {\n    const complement = target - nums[i];\n\n    if (map.has(complement)) {\n      return [map.get(complement), i];\n    }\n    map.set(nums[i], i);\n  }\n  return [];\n}\n\n// twoSum([2,7,11,15], 9) -> [0,1]\n// O(n) time, O(n) space",
         "The complement pattern in a hash map is the most common interview optimization technique."),

        ("INTERMEDIATE","Design a URL shortener system.",
         "Requirements: shorten URLs, redirect fast, handle 1M+ requests/day. Components: API server, ID generator (base62 of auto-increment), Redis (fast lookup), PostgreSQL (persistent store), CDN (redirect at edge).",
         "// ID generation (base62)\nconst CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';\nfunction encode(num) {\n  let result = '';\n  while (num > 0) {\n    result = CHARS[num % 62] + result;\n    num = Math.floor(num / 62);\n  }\n  return result.padStart(7, '0');\n}\n\n// Request flow:\n// POST /shorten -> generate ID -> store in DB + Redis\n// GET /:id -> Redis lookup (cache hit ~99%)\n//          -> 301 redirect to original URL",
         "Always start system design: requirements -> estimation -> high-level -> deep dive."),

        ("INTERMEDIATE","What is the difference between vertical and horizontal scaling?",
         "Vertical: add more CPU/RAM to one server. Simple but has hardware ceiling and single point of failure. Horizontal: add more servers behind a load balancer. No single point of failure, virtually unlimited scale, but requires stateless application design.",
         "// Horizontal scaling requires stateless services\n// Bad: session in memory (only one server has it)\napp.use(session({ secret: 'x', resave: false }));\n\n// Good: session in Redis (shared across servers)\napp.use(session({\n  store: new RedisStore({ client: redisClient }),\n  secret: process.env.SESSION_SECRET,\n  resave: false,\n}));\n\n// JWT is inherently stateless — even better",
         "Horizontal scaling + stateless design is the foundation of cloud-native architecture."),

        ("INTERMEDIATE","Explain caching strategies: cache-aside, write-through, write-behind.",
         "Cache-aside (lazy loading): check cache first; on miss, load DB and populate cache. Most common. Write-through: write to both cache and DB simultaneously — consistent but slower writes. Write-behind: write to cache immediately, async persist to DB — fastest writes, risk of loss on crash.",
         "// Cache-aside pattern\nasync function getUser(id) {\n  const key = 'user:' + id;\n  const cached = await redis.get(key);\n  if (cached) return JSON.parse(cached);\n\n  const user = await db.findById(id);\n  await redis.setex(key, 3600, JSON.stringify(user));\n  return user;\n}\n\n// Invalidate on update\nasync function updateUser(id, data) {\n  await db.update(id, data);\n  await redis.del('user:' + id);\n}",
         "Always set TTL on cached entries — never cache without expiry."),

        ("ADVANCED","How would you design a real-time notification system?",
         "Components: event producers, message broker (Kafka for scale), notification service (processes + routes), delivery channels (WebSocket for online, push/email/SMS for offline). Use fan-out pattern for broadcasting to many users.",
         "// Producer emits event\nawait kafka.send({\n  topic: 'notifications',\n  messages: [{ value: JSON.stringify({\n    type: 'ORDER_PLACED',\n    userId: user.id,\n    orderId: order.id\n  })}]\n});\n\n// Consumer routes notifications\nkafka.on('message', async msg => {\n  const event = JSON.parse(msg.value);\n  // WebSocket for online users\n  io.to('user:' + event.userId).emit('notification', {\n    type: event.type, message: 'Order confirmed!'\n  });\n  // Email for offline users\n  if (!onlineUsers.has(event.userId))\n    await emailQueue.add(event);\n});",
         "Separate notification routing from delivery — use dedicated workers per channel."),

        ("ADVANCED","Explain the CAP theorem.",
         "CAP states a distributed system can guarantee only 2 of 3: Consistency (all nodes see same data), Availability (every request gets a response), Partition Tolerance (works despite network failures). Since partitions are inevitable in distributed systems, real choice is CP or AP.",
         "// CP systems: MongoDB, ZooKeeper, HBase\n// During partition: refuse writes to stay consistent\n// Use when: bank balances, inventory counts\n\n// AP systems: Cassandra, DynamoDB, CouchDB\n// During partition: serve potentially stale data\n// Use when: social feeds, product catalog\n\n// Tunable consistency example (Cassandra):\nCONSISTENCY QUORUM; -- majority of nodes must agree\nCONSISTENCY EVENTUAL; -- fast, may read stale",
         "Modern systems often have configurable consistency (e.g., MongoDB readConcern/writeConcern)."),

        ("ADVANCED","Explain database connection pooling.",
         "Creating a new DB connection is expensive (TCP handshake, auth, memory). Connection pooling maintains a pool of pre-established connections reused across requests. Without pooling, high traffic exhausts DB connections. pg-pool (Postgres), Mongoose (MongoDB) pool by default.",
         "// PostgreSQL with pg pool\nconst { Pool } = require('pg');\n\nconst pool = new Pool({\n  host: process.env.DB_HOST,\n  database: process.env.DB_NAME,\n  user: process.env.DB_USER,\n  password: process.env.DB_PASS,\n  max: 20,          // max connections\n  idleTimeoutMillis: 30000,\n  connectionTimeoutMillis: 2000,\n});\n\n// Reuses existing connection from pool\nconst result = await pool.query(\n  'SELECT * FROM users WHERE id = $1', [id]\n);",
         "Tune max pool size based on DB max_connections. Rule: pool size = (number of cores * 2) + effective spindle count."),
    ],

    "Phase 6: Scalable Architecture & Production DevOps": [
        ("BASIC","What is the difference between monolithic and microservices architecture?",
         "Monolith: single deployable unit, all features in one codebase — simple for small teams. Microservices: independently deployable services, each owning its domain and database — enables independent scaling and team autonomy but adds operational complexity.",
         "// Monolith — one deployment\napp/\n  src/\n    auth/\n    users/\n    products/\n    payments/\n\n// Microservices — many deployments\nauth-service/     -> :3001\nuser-service/     -> :3002\nproduct-service/  -> :3003\npayment-service/  -> :3004\n// Each communicates via HTTP/gRPC/events\n// Each has its own database",
         "Most startups: start monolith, extract microservices when specific pain points appear."),

        ("BASIC","What is Docker and why is it used?",
         "Docker packages an application and all its dependencies into a container — a portable unit that runs identically everywhere. Solves 'works on my machine' problems. Containers share the host OS kernel (unlike VMs) so they start in seconds and use less resources.",
         "# Multi-stage Dockerfile for Next.js\nFROM node:20-alpine AS deps\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\n\nFROM deps AS builder\nCOPY . .\nRUN npm run build\n\nFROM node:20-alpine AS runner\nWORKDIR /app\nCOPY --from=builder /app/.next ./.next\nCOPY --from=builder /app/public ./public\nCOPY --from=deps /app/node_modules ./node_modules\nEXPOSE 3000\nCMD [\"npm\", \"start\"]",
         "Multi-stage builds keep images small by excluding build tools from the final image."),

        ("BASIC","What is CI/CD and why does it matter?",
         "CI (Continuous Integration): automatically test and build on every push, catching bugs early. CD (Continuous Deployment): automatically deploy passing builds to production. Together they reduce manual errors, speed up releases, and ensure consistent deployments.",
         "# .github/workflows/deploy.yml\nname: CI/CD Pipeline\non:\n  push:\n    branches: [main]\njobs:\n  test-and-deploy:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-node@v4\n        with: { node-version: '20' }\n      - run: npm ci\n      - run: npm test\n      - run: npm run build\n      - name: Deploy\n        run: |\n          ssh user@server 'cd /app &&\n            git pull && npm ci &&\n            npm run build &&\n            pm2 restart all'",
         "Never deploy to production without automated tests passing in CI."),

        ("INTERMEDIATE","What is load balancing? Explain load balancing algorithms.",
         "Load balancing distributes requests across multiple servers to prevent overload and enable scaling. Algorithms: Round Robin (rotate equally), Least Connections (route to least busy), IP Hash (consistent routing per user for session stickiness), Weighted (more traffic to stronger servers).",
         "# Nginx load balancer config\nupstream backend {\n  least_conn;\n\n  server app1.example.com:3000 weight=3;\n  server app2.example.com:3000 weight=2;\n  server app3.example.com:3000 weight=1;\n\n  keepalive 32;\n}\n\nserver {\n  listen 80;\n  location / {\n    proxy_pass http://backend;\n    proxy_set_header Host $host;\n    proxy_set_header X-Real-IP $remote_addr;\n    proxy_connect_timeout 5s;\n    proxy_read_timeout 30s;\n  }\n}",
         "Nginx, HAProxy (open source), AWS ALB, GCP Load Balancer, Cloudflare are popular options."),

        ("INTERMEDIATE","How does Redis work as a cache? Explain eviction policies.",
         "Redis is an in-memory key-value store with sub-millisecond latency. When memory is full, eviction policies determine what to remove. LRU (Least Recently Used) is most common for caches. allkeys-lru evicts any key; volatile-lru only evicts keys with TTL set.",
         "const redis = require('ioredis');\nconst client = new redis(process.env.REDIS_URL);\n\n// Set with 1-hour TTL\nawait client.setex('product:123', 3600,\n  JSON.stringify(product));\n\n// Get\nconst raw = await client.get('product:123');\nif (raw) return JSON.parse(raw);\n\n// Atomic operations\nawait client.incr('page:views:home');\nawait client.lpush('recent:products', productId);\nawait client.ltrim('recent:products', 0, 9); // keep 10",
         "Set maxmemory and maxmemory-policy in redis.conf. allkeys-lru is the standard cache policy."),

        ("INTERMEDIATE","What are message queues and when should you use them?",
         "Message queues decouple producers from consumers and handle async workloads. Use when: tasks are time-consuming (email, video processing), you need retry logic on failure, you need to absorb traffic spikes, or services need to communicate without tight coupling.",
         "const { Queue, Worker } = require('bullmq');\n\n// Producer — add to queue\nconst emailQueue = new Queue('email', { connection: redis });\n\nawait emailQueue.add('welcome', { userId }, {\n  attempts: 3,\n  backoff: { type: 'exponential', delay: 1000 }\n});\n\n// Consumer — process jobs\nnew Worker('email', async job => {\n  const { userId } = job.data;\n  const user = await db.findById(userId);\n  await mailer.sendWelcome(user.email);\n}, { connection: redis });",
         "BullMQ (Redis-based) is great for Node.js. For massive event streaming, use Apache Kafka."),

        ("INTERMEDIATE","Explain the production infrastructure flow for a scalable app.",
         "Request journey: User -> CDN (static + edge cache) -> Load Balancer -> App Servers (stateless) -> Cache Layer (Redis) -> Database (primary writes / replica reads). Background jobs go through message queues to workers.",
         "// Production flow:\n// 1. User hits CDN (Cloudflare/CloudFront)\n//    -> cached: serve immediately\n//    -> miss: forward to origin\n\n// 2. Load Balancer (Nginx/AWS ALB)\n//    -> distributes to app server pool\n\n// 3. App Server (stateless Next.js/Node)\n//    -> check Redis cache\n//    -> cache hit: return immediately\n//    -> cache miss: query PostgreSQL replica\n//    -> write operations: PostgreSQL primary\n\n// 4. Background tasks:\n//    -> BullMQ/Kafka -> Workers\n//    -> (email, notifications, analytics)",
         "Always make app servers stateless — store sessions, cache, and feature flags in Redis."),

        ("ADVANCED","What is Kubernetes and how does it orchestrate containers?",
         "Kubernetes (K8s) manages containers at scale: scheduling across nodes, self-healing (restarts failed pods), rolling deployments (zero downtime), HPA (auto-scaling), load balancing, service discovery, and secret management.",
         "# deployment.yaml\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: api\nspec:\n  replicas: 3\n  selector:\n    matchLabels: { app: api }\n  template:\n    spec:\n      containers:\n      - name: api\n        image: myregistry/api:v1.2.3\n        resources:\n          requests: { cpu: 100m, memory: 128Mi }\n          limits: { cpu: 500m, memory: 512Mi }\n---\n# Auto-scale 3-20 pods based on CPU\napiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nspec:\n  minReplicas: 3\n  maxReplicas: 20\n  metrics:\n  - type: Resource\n    resource:\n      name: cpu\n      target:\n        type: Utilization\n        averageUtilization: 70",
         "Start with Docker Compose for local dev. Graduate to Kubernetes when managing 5+ services."),

        ("ADVANCED","How would you design a system for 1 million concurrent users?",
         "Layer the architecture: CDN -> Load Balancer -> Stateless App Servers (auto-scaling) -> Redis Cache Cluster -> DB (primary + read replicas + sharding at extreme scale) -> Message Queues -> Background Workers -> Monitoring.",
         "// Capacity estimation for 1M users:\n// Peak: ~50K req/sec (assume 5% concurrent)\n// Avg response: 100ms -> 5000 RPS per server\n// -> Need ~10 app servers at peak\n// DB reads: 80% -> route to 3 replicas\n// DB writes: 20% -> primary\n// Cache hit rate target: 95%+\n\n// Auto-scaling rule:\n// Scale out when CPU > 70% for 2 minutes\n// Scale in when CPU < 30% for 5 minutes\n// Min: 3 instances (HA)\n// Max: 50 instances (cost cap)",
         "Always estimate: traffic -> server count -> DB connections -> cache hit rate -> infrastructure cost."),

        ("ADVANCED","Explain distributed tracing and observability.",
         "Observability has three pillars: Metrics (Prometheus), Logs (centralized logging), Traces (distributed request tracing). Distributed tracing tracks a request across services using a shared trace ID propagated in headers. Use OpenTelemetry as the standard instrumentation layer.",
         "// OpenTelemetry setup\nconst { trace } = require('@opentelemetry/api');\n\nasync function processOrder(orderId) {\n  const tracer = trace.getTracer('order-service');\n  const span = tracer.startSpan('processOrder');\n  span.setAttribute('order.id', orderId);\n\n  try {\n    const order = await db.findOrder(orderId);\n    span.addEvent('order.fetched');\n\n    await paymentService.charge(order);\n    span.setStatus({ code: SpanStatusCode.OK });\n  } catch (err) {\n    span.recordException(err);\n    span.setStatus({ code: SpanStatusCode.ERROR });\n    throw err;\n  } finally {\n    span.end();\n  }\n}",
         "Key SLIs to monitor: latency (p50/p95/p99), error rate (%), throughput (RPS), saturation (CPU/mem)."),

        ("ADVANCED","What is the Saga pattern in microservices?",
         "Saga manages distributed transactions across microservices that each own their own database (no shared DB, no SQL transactions). Choreography: services emit events that trigger other services. Orchestration: a central orchestrator calls services and handles compensating transactions on failure.",
         "// Orchestration Saga\nclass OrderSaga {\n  async execute(orderId) {\n    try {\n      await inventoryService.reserve(orderId);\n      await paymentService.charge(orderId);\n      await shippingService.schedule(orderId);\n      await notifyService.send(orderId);\n    } catch (err) {\n      // Compensate — rollback in reverse\n      await shippingService.cancel(orderId);\n      await paymentService.refund(orderId);\n      await inventoryService.release(orderId);\n      throw err;\n    }\n  }\n}",
         "Compensating transactions are the microservices equivalent of SQL ROLLBACK."),

        ("ADVANCED","What are common production engineering mistakes to avoid?",
         "1) No monitoring — blind when things break. 2) Hardcoded secrets — use environment variables and secret managers. 3) No rate limiting — open to brute force. 4) Unhandled promise rejections — crash Node processes. 5) No backups — catastrophic data loss. 6) No CI/CD — error-prone manual deploys. 7) Premature microservices — adds complexity before it's needed.",
         "// Handle all unhandled rejections\nprocess.on('unhandledRejection', (reason, promise) => {\n  logger.error('Unhandled rejection:', reason);\n  // Graceful shutdown\n  server.close(() => process.exit(1));\n});\n\n// Validate env vars on startup\nconst required = ['DB_URL','JWT_SECRET','REDIS_URL'];\nfor (const key of required) {\n  if (!process.env[key])\n    throw new Error(key + ' env var not set');\n}\n\n// Graceful shutdown\nprocess.on('SIGTERM', async () => {\n  await server.close();\n  await db.end();\n  process.exit(0);\n});",
         "Add a production readiness checklist: monitoring, logging, backups, secrets, rate limits, graceful shutdown."),
    ],

    "Phase 7: Testing & Quality Assurance": [
        ("BASIC","What is the difference between Unit, Integration, and End-to-End (E2E) testing?",
         "Unit: tests a single function/component in isolation (Jest). Integration: tests how multiple units work together (React Testing Library, API tests). E2E: simulates a real user journey in a real browser (Cypress, Playwright).",
         "// Unit\nexpect(sum(1, 2)).toBe(3);\n\n// Integration\nrender(<LoginForm />);\nuserEvent.type(screen.getByLabelText('Email'), 'test@test.com');\n\n// E2E\nawait page.goto('/login');\nawait page.fill('#email', 'test@test.com');",
         "The Testing Pyramid suggests many Unit tests, some Integration tests, and fewer E2E tests (as they are slow and brittle)."),

        ("INTERMEDIATE","Explain React Testing Library vs Enzyme.",
         "Enzyme tests implementation details (state, props, component internals). React Testing Library tests behavior from the user's perspective (finding elements by role, text, or label). RTL is the modern standard because it makes tests resilient to refactoring.",
         "// Bad (Enzyme approach - testing internals)\nwrapper.setState({ count: 1 });\nexpect(wrapper.state('count')).toBe(1);\n\n// Good (RTL approach - testing behavior)\nrender(<Counter />);\nfireEvent.click(screen.getByRole('button', { name: /increment/i }));\nexpect(screen.getByText('Count: 1')).toBeInTheDocument();",
         "Always try to query by accessibility roles first (e.g. getByRole). It ensures your app is accessible too."),

        ("ADVANCED","How do you mock API calls in tests?",
         "Avoid making real network requests in tests. You can mock fetch/axios directly with Jest (jest.mock). Better yet, use MSW (Mock Service Worker) which intercepts network requests at the network level and returns mock responses — it works identically for tests and local development.",
         "import { rest } from 'msw';\nimport { setupServer } from 'msw/node';\n\nconst server = setupServer(\n  rest.get('/api/user', (req, res, ctx) => {\n    return res(ctx.json({ name: 'John' }));\n  })\n);\n\nbeforeAll(() => server.listen());\nafterEach(() => server.resetHandlers());\nafterAll(() => server.close());",
         "MSW is the industry standard for mocking APIs in modern frontend testing. Mention it to stand out."),
    ],
}

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
    story.append(Spacer(1, 30*mm))

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
    
    story.append(Paragraph("MERN Stack &amp; Next.js  |  Mid-Level &amp; Above", meta_s))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("7 Phases  |  100+ Questions  |  Basic to Advanced", meta_light))
    
    story.append(Spacer(1, 15*mm))
    
    # Author Info
    story.append(Paragraph("Curated by N.I. Nazmul", author_title))
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph("Full-Stack Developer (MERN Stack &amp; Next.js Specialist)", author_sub))
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph("github.com/ninazmul", author_sub))

    story.append(Spacer(1, 15*mm))

    phases = [
        ("Phase 1", "JavaScript &\nTypeScript"),
        ("Phase 2", "React &\nNext.js"),
        ("Phase 3", "Node.js &\nExpress"),
        ("Phase 4", "MongoDB &\nPostgreSQL"),
        ("Phase 5", "System Design\n& DSA"),
        ("Phase 6", "Architecture\n& DevOps"),
        ("Phase 7", "Testing &\nQA"),
    ]
    colors_list = [BLUE, GREEN, PURPLE, AMBER, CORAL, PINK, TEAL]
    bg_list = [LBLUE, LGREEN, LPURPLE, LAMBER, LCORAL, LPINK, LTEAL]

    cw = (W - 40*mm) / 3
    for row_idx in range(0, len(phases), 3):
        row_data = []
        row_colors = []
        for j in range(3):
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

        tbl = Table([row_data], colWidths=[cw]*3, rowHeights=[22*mm])
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

def build_question(story, q_num, level, question, answer, code, tip):
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

    header = Table(
        [[Paragraph(f"Q{q_num}", num_s), Paragraph(level, lvl_s)]],
        colWidths=[W - 60*mm - 26*mm, 26*mm]
    )
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), lbg),
        ('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
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
    "/Users/n.i.nazmul/Downloads/FullStack_Interview_QnA.pdf",
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=16*mm, bottomMargin=22*mm,
    title="Full-Stack Developer Interview Q&A — MERN & Next.js",
    author="Interview Prep Guide",
    subject="Mid-level Full-Stack Developer Interview Preparation",
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

    for level, question, answer, code, tip in questions:
        build_question(story, q_num, level, question, answer, code, tip)
        q_num += 1

doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
print(f"Done! Generated {q_num-1} questions across {len(QNA)} phases.")

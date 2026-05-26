# Skyvern SDK Reference — Full Docs
Scraped: Tue, May 26, 2026  3:00:03 AM


---
## sdk-reference/overview
Source: https://skyvern.com/docs/sdk-reference/overview.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Overview

The Skyvern SDK wraps the REST API in a typed client with built-in browser automation via Playwright.

\## Install

 \`\`\`bash Python theme={null}
 # Requires Python 3.11+
 pip install skyvern
 \`\`\`

 \`\`\`bash TypeScript theme={null}
 # Requires Node.js 18+ (also compatible with Bun, Deno, and Cloudflare Workers)
 npm install @skyvern/client
 \`\`\`

 If you hit Python version errors, use \`pipx install skyvern\` to install in an isolated environment.

\\*\\*\\*

\## Initialize the client

Create a \`Skyvern\` instance with your API key. All methods are async.

 \`\`\`python Python theme={null}
 import asyncio
 from skyvern import Skyvern

 async def main():
 # All methods are coroutines - wrap in async and use asyncio.run()
 # If inside FastAPI/Django ASGI, await directly without asyncio.run()
 client = Skyvern(api\_key="YOUR\_API\_KEY")

 result = await client.run\_task(
 prompt="Get the title of the top post on Hacker News",
 url="https://news.ycombinator.com",
 wait\_for\_completion=True,
 )
 print(result.output)

 asyncio.run(main())
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { Skyvern } from "@skyvern/client";

 // All methods return promises
 const skyvern = new Skyvern({ apiKey: "YOUR\_API\_KEY" });

 const result = await skyvern.runTask({
 body: {
 prompt: "Get the title of the top post on Hacker News",
 url: "https://news.ycombinator.com",
 },
 waitForCompletion: true,
 });
 console.log(result.output);
 \`\`\`

\### Constructor parameters

\| Parameter \| Type \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`api\_key\` / \`apiKey\` \| \`str\` / \`string\` \| - \| \*\*Required.\*\* Your Skyvern API key. Get one at \[app.skyvern.com/settings\](https://app.skyvern.com/settings/). \|
\| \`environment\` \| \`SkyvernEnvironment\` \| \`CLOUD\` / \`Cloud\` \| Target environment. See \[Environments\](#environments). \|
\| \`base\_url\` / \`baseUrl\` \| \`str\` / \`string\` \| \`None\` \| Override the API base URL for self-hosted deployments. \|
\| \`timeout\` / \`timeoutInSeconds\` \| \`float\` / \`number\` \| \`None\` / \`60\` \| HTTP request timeout in seconds. \|
\| \`max\_retries\` / \`maxRetries\` \| \`int\` / \`number\` \| \`None\` / \`2\` \| Number of times to retry failed requests. \|
\| \`headers\` \| \`dict\` / \`Record\` \| \`None\` \| Additional headers included with every request. \|

 \| Parameter \| Type \| Default \| Description \|
 \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
 \| \`follow\_redirects\` \| \`bool\` \| \`True\` \| Whether to follow HTTP redirects. \|
 \| \`httpx\_client\` \| \`httpx.AsyncClient\` \| \`None\` \| Provide your own httpx client for custom TLS, proxying, or connection pooling. \|

\\*\\*\\*

\## Environments

Three built-in environment URLs:

 \`\`\`python Python theme={null}
 from skyvern.client import SkyvernEnvironment
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { SkyvernEnvironment } from "@skyvern/client";
 \`\`\`

\| Environment \| URL \| When to use \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`CLOUD\` / \`Cloud\` \| \`https://api.skyvern.com\` \| Skyvern Cloud (default) \|
\| \`STAGING\` / \`Staging\` \| \`https://api-staging.skyvern.com\` \| Staging environment \|
\| \`LOCAL\` / \`Local\` \| \`http://localhost:8000\` \| Local server started with \`skyvern run server\` \|

For a self-hosted instance at a custom URL:

 \`\`\`python Python theme={null}
 client = Skyvern(
 api\_key="YOUR\_API\_KEY",
 base\_url="https://skyvern.your-company.com",
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const skyvern = new Skyvern({
 apiKey: "YOUR\_API\_KEY",
 baseUrl: "https://skyvern.your-company.com",
 });
 \`\`\`

\\*\\*\\*

\## Local mode

Run Skyvern entirely on your machine - no cloud, no network calls. \`Skyvern.local()\` reads your \`.env\` file, boots the engine in-process, and connects the client to it.

\*\*Prerequisite:\*\* Run \`skyvern quickstart\` once to create the \`.env\` file with your database connection and LLM API keys.

\`\`\`python theme={null}
from skyvern import Skyvern

\# Python only. TypeScript requires a running Skyvern server
client = Skyvern.local()

result = await client.run\_task(
 prompt="Get the title of the top post",
 url="https://news.ycombinator.com",
 wait\_for\_completion=True,
)
\`\`\`

If you configured headful mode during \`skyvern quickstart\`, a Chromium window opens so you can watch the AI work.

\| Parameter \| Type \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`llm\_config\` \| \`LLMConfig \\\| LLMRouterConfig \\\| None\` \| \`None\` \| Override the LLM. If omitted, uses \`LLM\_KEY\` from \`.env\`. \|
\| \`settings\` \| \`dict \\\| None\` \| \`None\` \| Override \`.env\` settings at runtime. Example: \`{"MAX\_STEPS\_PER\_RUN": 100}\` \|

\\*\\*\\*

\## Waiting for completion

By default, task and workflow runs return immediately after queuing. You get a run ID and need to poll for results yourself. Pass \`wait\_for\_completion\` to have the SDK poll automatically until the run reaches a terminal state (\`completed\`, \`failed\`, \`terminated\`, \`timed\_out\`, or \`canceled\`):

 \`\`\`python Python theme={null}
 # Returns only after the task finishes (up to 30 min by default)
 result = await client.run\_task(
 prompt="Fill out the contact form",
 url="https://example.com/contact",
 wait\_for\_completion=True,
 timeout=600, # give up after 10 minutes
 )

 # Without wait\_for\_completion -- returns immediately
 task = await client.run\_task(
 prompt="Fill out the contact form",
 url="https://example.com/contact",
 )
 print(task.run\_id) # poll with client.get\_run(task.run\_id)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Returns only after the task finishes (up to 30 min by default)
 const result = await skyvern.runTask({
 body: {
 prompt: "Fill out the contact form",
 url: "https://example.com/contact",
 },
 waitForCompletion: true,
 timeout: 600, // give up after 10 minutes
 });

 // Without waitForCompletion -- returns immediately
 const task = await skyvern.runTask({
 body: {
 prompt: "Fill out the contact form",
 url: "https://example.com/contact",
 },
 });
 console.log(task.run\_id); // poll with skyvern.getRun(task.run\_id)
 \`\`\`

\| Parameter \| Type \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`wait\_for\_completion\` / \`waitForCompletion\` \| \`bool\` / \`boolean\` \| \`false\` \| Poll until the run finishes. \|
\| \`timeout\` \| \`float\` / \`number\` \| \`1800\` \| Maximum wait time in seconds. \|

Supported on task runs, workflow runs, and login. In TypeScript, also supported on file downloads.

\\*\\*\\*

\## Request options

Every method accepts per-request overrides for timeout, retries, and headers:

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 result = await client.run\_task(
 prompt="Extract data",
 url="https://example.com",
 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 ),
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 const result = await skyvern.runTask(
 {
 body: {
 prompt: "Extract data",
 url: "https://example.com",
 },
 },
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 },
 );
 \`\`\`

\| Option \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` / \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout for this request. \|
\| \`max\_retries\` / \`maxRetries\` \| \`int\` / \`number\` \| Retry count for this request. \|
\| \`additional\_headers\` / \`headers\` \| \`dict\` / \`Record\` \| Extra headers for this request. \|
\| \`additional\_query\_parameters\` \| \`dict\` \| Extra query parameters (Python only). \|
\| \`additional\_body\_parameters\` \| \`dict\` \| Extra body parameters (Python only). \|
\| \`abortSignal\` \| \`AbortSignal\` \| Signal to abort the request (TypeScript only). \|
\| \`apiKey\` \| \`string\` \| Override the API key for this request (TypeScript only). \|

These override the client-level defaults for that single call only.

\\*\\*\\*

\## Next steps

 Control browsers with Playwright + AI

 Run browser automations with \`run\_task\`

 Create and run multi-step automations

 Handle errors and configure retries

---
## sdk-reference/complete-reference
Source: https://skyvern.com/docs/sdk-reference/complete-reference.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Complete Reference (For LLMs)

\> Complete reference for every method, parameter, and type in the Skyvern Python SDK. Includes tasks, workflows, browser sessions, browser profiles, credentials, helper methods, browser control, and error handling in a single page.

\## Install and initialize

 \`\`\`bash Python theme={null}
 # Requires Python 3.11+
 pip install skyvern
 \`\`\`

 \`\`\`bash TypeScript theme={null}
 # Requires Node.js 18+
 npm install @skyvern/client
 \`\`\`

 \`\`\`python Python theme={null}
 import asyncio
 from skyvern import Skyvern

 async def main():
 client = Skyvern(api\_key="YOUR\_API\_KEY")
 result = await client.run\_task(
 prompt="Get the title of the top post on Hacker News",
 url="https://news.ycombinator.com",
 wait\_for\_completion=True,
 )
 print(result.output)

 asyncio.run(main())
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { Skyvern } from "@skyvern/client";

 const skyvern = new Skyvern({ apiKey: "YOUR\_API\_KEY" });

 const result = await skyvern.runTask({
 body: {
 prompt: "Get the title of the top post on Hacker News",
 url: "https://news.ycombinator.com",
 },
 waitForCompletion: true,
 });
 console.log(result.output);
 \`\`\`

\*\*Constructor:\*\*

 \`\`\`python Python theme={null}
 Skyvern(
 api\_key: str, # Required
 base\_url: str \| None = None, # Override for self-hosted deployments
 environment: SkyvernEnvironment = CLOUD,# CLOUD, STAGING, or LOCAL
 timeout: float \| None = None, # HTTP request timeout (seconds)
 )

 # Local mode (Python only - runs entirely on your machine, reads .env)
 client = Skyvern.local()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 new Skyvern({
 apiKey: string, // Required
 baseUrl?: string, // Override for self-hosted deployments
 environment?: SkyvernEnvironment \| string, // Cloud (default), Staging, or Local
 timeoutInSeconds?: number, // HTTP request timeout (default: 60)
 maxRetries?: number, // Retry count (default: 2)
 headers?: Record, // Additional headers
 })
 \`\`\`

\\*\\*\\*

\## Browser Automation

\### SkyvernBrowser

 \`\`\`python Python theme={null}
 # Launch / connect
 browser = await client.launch\_cloud\_browser(timeout=60, proxy\_location=None)
 browser = await client.use\_cloud\_browser(timeout=60, proxy\_location=None)
 browser = await client.connect\_to\_cloud\_browser\_session("pbs\_abc123")
 browser = await client.connect\_to\_browser\_over\_cdp("http://localhost:9222")
 browser = await client.launch\_local\_browser(headless=False, port=9222) # Python only

 # Get pages
 page = await browser.get\_working\_page() # Most recent page, or creates one
 page = await browser.new\_page() # Always creates a new tab
 page = await browser.get\_page\_for(pw\_page) # Wrap existing Playwright Page (Python only)
 await browser.close() # Close browser and cloud session
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Launch / connect
 const browser = await skyvern.launchCloudBrowser({ timeout: 60 });
 const browser = await skyvern.useCloudBrowser({ timeout: 60 });
 const browser = await skyvern.connectToCloudBrowserSession("pbs\_abc123");
 const browser = await skyvern.connectToBrowserOverCdp("http://localhost:9222");
 // launch\_local\_browser - Python only, no TS equivalent

 // Get pages
 const page = await browser.getWorkingPage(); // Most recent page, or creates one
 const page = await browser.newPage(); // Always creates a new tab
 // get\_page\_for - Python only, no TS equivalent
 await browser.close(); // Close browser and cloud session
 \`\`\`

\### SkyvernPage

AI-enhanced Playwright methods - pass a selector for standard Playwright, add a prompt for AI fallback, or use prompt alone for pure AI.

 \`\`\`python Python theme={null}
 # act - freeform AI action
 await page.act("Click the login button")

 # extract - structured data extraction
 data = await page.extract("Extract all products", schema={...})

 # validate - page state assertion, returns bool
 ok = await page.validate("User is logged in")

 # prompt - ask LLM about the page
 result = await page.prompt("What is the heading?", schema={...})

 # locator - AI element locator returning chainable AILocator (Python only)
 locator = page.locator(prompt="the submit button")
 await locator.click()

 # click - selector, AI, or both with fallback
 await page.click("#submit-btn")
 await page.click(prompt="Click the submit button")
 await page.click("#submit-btn", prompt="Click submit")

 # fill - selector, AI, or both with fallback
 await page.fill("#email", value="user@example.com")
 await page.fill(prompt="Fill email with user@example.com")

 # select\_option - selector, AI, or both with fallback
 await page.select\_option("#country", value="us")
 await page.select\_option(prompt="Select United States")

 # type - character-by-character input (Python only)
 await page.type("#search", value="query")

 # hover (Python only)
 await page.hover("#menu-item", intention="Hover over the menu")

 # scroll (Python only)
 await page.scroll(0, 500)

 # upload\_file (Python only)
 await page.upload\_file("#file-input", files="/path/to/file.pdf")

 # fill\_form - AI full form fill (Python only)
 await page.fill\_form(data={"name": "John", "email": "john@example.com"})

 # fill\_multipage\_form - across page transitions (Python only)
 await page.fill\_multipage\_form(data={...}, max\_pages=5)

 # fill\_from\_mapping - explicit field→value mapping (Python only)
 await page.fill\_from\_mapping(form\_fields=fields, mapping={0: "John"}, data={...})

 # extract\_form\_fields - get all fields with metadata (Python only)
 fields = await page.extract\_form\_fields()

 # validate\_mapping - verify mapping works (Python only)
 is\_valid = await page.validate\_mapping(form\_fields=fields, mapping={...}, prompt="Validate fields")

 # fill\_autocomplete - typeahead handling (Python only)
 await page.fill\_autocomplete(selector="#city", value="San Francisco")

 # frame\_switch - switch iframe context (Python only)
 await page.frame\_switch(selector="#payment-iframe")
 page.frame\_main() # back to main frame
 frames = await page.frame\_list() # list all frames
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // act - freeform AI action
 await page.act("Click the login button");

 // extract - structured data extraction
 const data = await page.extract({ prompt: "Extract all products", schema: {...} });

 // validate - page state assertion, returns boolean
 const ok = await page.validate("User is logged in");

 // prompt - ask LLM about the page
 const result = await page.prompt("What is the heading?", { heading: { type: "string" } });

 // find / AILocator - Python only, no TS equivalent

 // click - selector, AI, or both with fallback
 await page.click("#submit-btn");
 await page.click({ prompt: "Click the submit button" });
 await page.click("#submit-btn", { prompt: "Click submit" });

 // fill - selector, AI, or both with fallback
 await page.fill("#email", "user@example.com");
 await page.fill({ prompt: "Fill email with user@example.com" });

 // selectOption - selector, AI, or both with fallback
 await page.selectOption("#country", "us");
 await page.selectOption({ prompt: "Select United States" });

 // type, hover, scroll, upload\_file - Python only
 // fill\_form, fill\_multipage\_form, fill\_from\_mapping - Python only
 // extract\_form\_fields, validate\_mapping, fill\_autocomplete - Python only
 // frame\_switch, frame\_main, frame\_list - Python only
 \`\`\`

\### Page Agent

Full task/workflow execution in the context of the current page. Always waits for completion.

 \`\`\`python Python theme={null}
 # run\_task
 result = await page.agent.run\_task("Fill out the form", data\_extraction\_schema={...}, max\_steps=10, timeout=1800)

 # login - supports skyvern, bitwarden, onepassword, azure\_vault
 await page.agent.login(credential\_type=CredentialType.skyvern, credential\_id="cred\_123")

 # download\_files
 result = await page.agent.download\_files("Download the invoice PDF", download\_suffix=".pdf")

 # run\_workflow
 result = await page.agent.run\_workflow("wpid\_abc123", parameters={"key": "value"})
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // runTask
 const result = await page.agent.runTask("Fill out the form", {
 dataExtractionSchema: {...}, maxSteps: 10, timeout: 1800,
 });

 // login - supports skyvern, bitwarden, 1password, azure\_vault
 await page.agent.login("skyvern", { credentialId: "cred\_123" });

 // downloadFiles
 const result = await page.agent.downloadFiles("Download the invoice PDF", {
 downloadSuffix: ".pdf",
 });

 // runWorkflow
 const result = await page.agent.runWorkflow("wpid\_abc123", {
 parameters: { key: "value" },
 });
 \`\`\`

\\*\\*\\*

\## Tasks

\### run\\\_task

 \`\`\`python Python theme={null}
 result = await client.run\_task(
 prompt: str, # Required
 url: str \| None = None,
 engine: RunEngine = RunEngine.skyvern\_v2,
 wait\_for\_completion: bool = False,
 timeout: float = 1800,
 max\_steps: int \| None = None,
 data\_extraction\_schema: dict \| str \| None = None,
 browser\_session\_id: str \| None = None,
 publish\_workflow: bool = False,
 proxy\_location: ProxyLocation \| None = None,
 webhook\_url: str \| None = None,
 error\_code\_mapping: dict\[str, str\] \| None = None,
 totp\_identifier: str \| None = None,
 totp\_url: str \| None = None,
 title: str \| None = None,
 model: dict \| None = None,
 user\_agent: str \| None = None,
 extra\_http\_headers: dict\[str, str\] \| None = None,
 include\_action\_history\_in\_verification: bool \| None = None,
 max\_screenshot\_scrolls: int \| None = None,
 browser\_address: str \| None = None,
 run\_with: str \| None = None,
 ) -\> TaskRunResponse
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: string, // Required
 url?: string,
 engine?: RunEngine, // "skyvern\_v2" default
 max\_steps?: number,
 data\_extraction\_schema?: Record \| string,
 browser\_session\_id?: string,
 publish\_workflow?: boolean,
 proxy\_location?: ProxyLocation,
 webhook\_url?: string,
 error\_code\_mapping?: Record,
 totp\_identifier?: string,
 totp\_url?: string,
 title?: string,
 model?: Record,
 user\_agent?: string,
 extra\_http\_headers?: Record,
 browser\_address?: string,
 run\_with?: string,
 },
 waitForCompletion?: boolean,
 timeout?: number, // Default: 1800
 }): Promise
 \`\`\`

\*\*TaskRunResponse:\*\* \`run\_id\`, \`status\`, \`output\`, \`failure\_reason\`, \`downloaded\_files\`, \`recording\_url\`, \`screenshot\_urls\`, \`app\_url\`, \`step\_count\`, \`script\_run\`, \`created\_at\`, \`finished\_at\`

\### get\\\_run

\`\`\`
get\_run(run\_id) → GetRunResponse
\`\`\`

\### cancel\\\_run

\`\`\`
cancel\_run(run\_id)
\`\`\`

\### get\\\_run\\\_timeline

\`\`\`
get\_run\_timeline(run\_id) → list\[WorkflowRunTimeline\]
\`\`\`

\### get\\\_run\\\_artifacts

\`\`\`
get\_run\_artifacts(run\_id, artifact\_type?) → list\[Artifact\]
\`\`\`

\### get\\\_artifact

\`\`\`
get\_artifact(artifact\_id) → Artifact
\`\`\`

\### get\\\_runs\\\_v2

\`\`\`
get\_runs\_v2(page?, page\_size?, status?, search\_key?) → list\[TaskRunListItem\]
\`\`\`

\### retry\\\_run\\\_webhook

\`\`\`
retry\_run\_webhook(run\_id, webhook\_url?)
\`\`\`

\\*\\*\\*

\## Workflows

\### run\\\_workflow

 \`\`\`python Python theme={null}
 result = await client.run\_workflow(
 workflow\_id: str, # Required. Permanent ID (wpid\_...).
 parameters: dict \| None = None,
 wait\_for\_completion: bool = False,
 timeout: float = 1800,
 run\_with: str \| None = None, # "code" or "agent"
 ai\_fallback: bool \| None = None,
 browser\_session\_id: str \| None = None,
 browser\_profile\_id: str \| None = None,
 proxy\_location: ProxyLocation \| None = None,
 max\_steps\_override: int \| None = None,
 webhook\_url: str \| None = None,
 title: str \| None = None,
 template: bool \| None = None,
 totp\_identifier: str \| None = None,
 totp\_url: str \| None = None,
 user\_agent: str \| None = None,
 extra\_http\_headers: dict\[str, str\] \| None = None,
 max\_screenshot\_scrolls: int \| None = None,
 browser\_address: str \| None = None,
 ) -\> WorkflowRunResponse
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runWorkflow({
 body: {
 workflow\_id: string, // Required
 parameters?: Record,
 browser\_session\_id?: string,
 browser\_profile\_id?: string,
 proxy\_location?: ProxyLocation,
 webhook\_url?: string,
 title?: string,
 totp\_identifier?: string,
 totp\_url?: string,
 user\_agent?: string,
 extra\_http\_headers?: Record,
 browser\_address?: string,
 ai\_fallback?: boolean,
 run\_with?: string,
 },
 template?: boolean,
 waitForCompletion?: boolean,
 timeout?: number, // Default: 1800
 }): Promise
 \`\`\`

\*\*WorkflowRunResponse:\*\* Same as TaskRunResponse plus \`run\_with\`, \`ai\_fallback\`, \`script\_run\`.

\### create\\\_workflow

\`\`\`
create\_workflow(json\_definition?, yaml\_definition?, folder\_id?) → Workflow
\`\`\`

\### get\\\_workflow

\`\`\`
get\_workflow(workflow\_permanent\_id, version?, template?) → Workflow
\`\`\`

\### get\\\_workflows

\`\`\`
get\_workflows(page?, page\_size?, only\_saved\_tasks?, only\_workflows?, only\_templates?, title?, search\_key?, folder\_id?, status?, template?) → list\[Workflow\]
\`\`\`

\### get\\\_workflow\\\_versions

\`\`\`
get\_workflow\_versions(workflow\_permanent\_id, template?) → list\[Workflow\]
\`\`\`

\### update\\\_workflow

\`\`\`
update\_workflow(workflow\_id, json\_definition?, yaml\_definition?) → Workflow
\`\`\`

\### delete\\\_workflow

\`\`\`
delete\_workflow(workflow\_id)
\`\`\`

\### get\\\_workflow\\\_runs

\`\`\`
get\_workflow\_runs(page?, page\_size?, status?, search\_key?, error\_code?) → list\[WorkflowRun\]
\`\`\`

\### update\\\_workflow\\\_folder

\`\`\`
update\_workflow\_folder(workflow\_permanent\_id, folder\_id?) → Workflow
\`\`\`

\*\*Workflow fields:\*\* \`workflow\_id\`, \`workflow\_permanent\_id\`, \`version\`, \`title\`, \`workflow\_definition\`, \`status\`, \`created\_at\`

\\*\\*\\*

\## Browser Sessions

\### create\\\_browser\\\_session

\`\`\`
create\_browser\_session(timeout?, proxy\_location?, extensions?, browser\_type?, browser\_profile\_id?) → BrowserSessionResponse
\`\`\`

\### get\\\_browser\\\_session

\`\`\`
get\_browser\_session(browser\_session\_id) → BrowserSessionResponse
\`\`\`

\### get\\\_browser\\\_sessions

\`\`\`
get\_browser\_sessions() → list\[BrowserSessionResponse\]
\`\`\`

\### close\\\_browser\\\_session

\`\`\`
close\_browser\_session(browser\_session\_id)
\`\`\`

\*\*BrowserSessionResponse fields:\*\* \`browser\_session\_id\`, \`status\`, \`browser\_address\`, \`app\_url\`, \`timeout\`, \`started\_at\`, \`created\_at\`

\\*\\*\\*

\## Browser Profiles

\### create\\\_browser\\\_profile

\`\`\`
create\_browser\_profile(name, description?, workflow\_run\_id?, browser\_session\_id?) → BrowserProfile
\`\`\`

\### list\\\_browser\\\_profiles

\`\`\`
list\_browser\_profiles(include\_deleted?) → list\[BrowserProfile\]
\`\`\`

\### get\\\_browser\\\_profile

\`\`\`
get\_browser\_profile(profile\_id) → BrowserProfile
\`\`\`

\### delete\\\_browser\\\_profile

\`\`\`
delete\_browser\_profile(profile\_id)
\`\`\`

\*\*BrowserProfile fields:\*\* \`browser\_profile\_id\`, \`name\`, \`description\`, \`created\_at\`

\\*\\*\\*

\## Credentials

\### create\\\_credential

\`\`\`
create\_credential(name, credential\_type, credential, vault\_type?) → CredentialResponse
\`\`\`

\### get\\\_credential

\`\`\`
get\_credential(credential\_id) → CredentialResponse
\`\`\`

\### get\\\_credentials

\`\`\`
get\_credentials(page?, page\_size?, vault\_type?) → list\[CredentialResponse\]
\`\`\`

\### update\\\_credential

\`\`\`
update\_credential(credential\_id, name, credential\_type, credential, vault\_type?) → CredentialResponse
\`\`\`

\### delete\\\_credential

\`\`\`
delete\_credential(credential\_id)
\`\`\`

\### send\\\_totp\\\_code

\`\`\`
send\_totp\_code(totp\_identifier, content, task\_id?, workflow\_id?, workflow\_run\_id?, source?, expired\_at?, type?) → TotpCode
\`\`\`

\\*\\*\\*

\## Helpers

\### login

\`\`\`
login(credential\_type, url?, credential\_id?, prompt?, browser\_session\_id?, browser\_profile\_id?, browser\_address?, proxy\_location?, webhook\_url?, totp\_identifier?, totp\_url?, extra\_http\_headers?, max\_screenshot\_scrolling\_times?, wait\_for\_completion?, timeout?) → WorkflowRunResponse
\`\`\`

Credential-specific parameters: \`bitwarden\_collection\_id\`, \`bitwarden\_item\_id\`, \`onepassword\_vault\_id\`, \`onepassword\_item\_id\`, \`azure\_vault\_name\`, \`azure\_vault\_username\_key\`, \`azure\_vault\_password\_key\`, \`azure\_vault\_totp\_secret\_key\`.

\### download\\\_files

\`\`\`
download\_files(navigation\_goal, url?, browser\_session\_id?, browser\_profile\_id?, proxy\_location?, webhook\_url?, download\_suffix?, download\_timeout?, max\_steps\_per\_run?, extra\_http\_headers?, totp\_identifier?, totp\_url?, browser\_address?, max\_screenshot\_scrolling\_times?) → WorkflowRunResponse
\`\`\`

Python does not support \`wait\_for\_completion\` - poll with \`get\_run()\`. TypeScript supports \`waitForCompletion\`.

\### upload\\\_file

\`\`\`
upload\_file(file) → UploadFileResponse
\`\`\`

Returns \`s3uri\` and \`presigned\_url\`.

\\*\\*\\*

\## Error Handling

 \`\`\`python Python theme={null}
 from skyvern.client.core import ApiError
 from skyvern.client.errors import NotFoundError

 try:
 run = await client.get\_run("tsk\_nonexistent")
 except NotFoundError as e:
 print(e.status\_code, e.body) # 404
 except ApiError as e:
 print(e.status\_code, e.body) # Any other HTTP error
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { SkyvernError, SkyvernTimeoutError, SkyvernApi } from "@skyvern/client";

 try {
 const run = await skyvern.getRun("tsk\_nonexistent");
 } catch (e) {
 if (e instanceof SkyvernApi.NotFoundError) {
 console.log(e.statusCode, e.body); // 404
 } else if (e instanceof SkyvernError) {
 console.log(e.statusCode, e.body); // Any other HTTP error
 }
 }
 \`\`\`

\*\*Error types:\*\* \`BadRequestError\` (400), \`ForbiddenError\` (403), \`NotFoundError\` (404), \`ConflictError\` (409), \`UnprocessableEntityError\` (422). All inherit from \`ApiError\` (Python) or \`SkyvernError\` (TypeScript).

Run failure is not an exception - check \`result.status\` (\`completed\`, \`failed\`, \`terminated\`, \`timed\_out\`, \`canceled\`).

\\*\\*\\*

\## Request options

Every method accepts \`request\_options\` (Python) or a second options argument (TypeScript) for per-request overrides:

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 abortSignal: controller.signal, // TypeScript only
 apiKey: "override-key", // TypeScript only
 }
 \`\`\`

\\*\\*\\*

\## Key constraints

\\* \`browser\_profile\_id\` works with \`run\_workflow\` only - silently ignored by \`run\_task\`.
\\* Python \`download\_files\` does not support \`wait\_for\_completion\` - poll manually or use webhooks.
\\* Only workflow runs with \`persist\_browser\_session=True\` produce archives for profile creation.
\\* \`launch\_local\_browser\` requires Python local mode (\`Skyvern.local()\`).
\\* \`page.agent\` methods always wait for completion.
\\* Python-only features: \`launch\_local\_browser\`, \`get\_page\_for\`, \`locator\`/\`AILocator\`, \`type\`, \`hover\`, \`scroll\`, \`upload\_file\` (page-level), form automation (\`fill\_form\`, \`fill\_multipage\_form\`, \`fill\_from\_mapping\`, \`extract\_form\_fields\`, \`validate\_mapping\`, \`fill\_autocomplete\`), iframe management (\`frame\_switch\`, \`frame\_main\`, \`frame\_list\`).

---
## sdk-reference/error-handling
Source: https://skyvern.com/docs/sdk-reference/error-handling.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Error Handling

\> Handle API errors, timeouts, and configure retries in the Skyvern Python SDK. Covers error types, exception handling, HTTP and completion timeouts, retry configuration, and run failure vs API error patterns.

The SDK raises typed exceptions for API errors. In Python, all errors extend \`ApiError\`. In TypeScript, all errors extend \`SkyvernError\`. Both include the HTTP status code, response body, and headers.

\\*\\*\\*

\## Error types

\| Exception \| Status Code \| When it's raised \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`BadRequestError\` \| 400 \| Invalid request parameters. \|
\| \`ForbiddenError\` \| 403 \| Invalid or missing API key. \|
\| \`NotFoundError\` \| 404 \| Resource (run, workflow, session) not found. \|
\| \`ConflictError\` \| 409 \| Resource conflict (e.g., duplicate creation). \|
\| \`UnprocessableEntityError\` \| 422 \| Request validation failed. \|
\| \`ApiError\` (Python) / \`SkyvernError\` (TS) \| Any \| Base class for all API errors. Catch this as a fallback. \|
\| \`SkyvernTimeoutError\` (TS only) \| - \| HTTP request timed out. \|

Import errors from the package:

 \`\`\`python Python theme={null}
 from skyvern.client.core import ApiError
 from skyvern.client.errors import (
 BadRequestError,
 ForbiddenError,
 NotFoundError,
 ConflictError,
 UnprocessableEntityError,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { SkyvernError, SkyvernTimeoutError, SkyvernApi } from "@skyvern/client";

 // Base errors are top-level exports:
 // SkyvernError - base class for all API errors
 // SkyvernTimeoutError - HTTP request timed out

 // HTTP status error subclasses are accessed via the SkyvernApi namespace:
 // SkyvernApi.BadRequestError - 400
 // SkyvernApi.ForbiddenError - 403
 // SkyvernApi.NotFoundError - 404
 // SkyvernApi.ConflictError - 409
 // SkyvernApi.UnprocessableEntityError - 422
 \`\`\`

The specific Python error classes live in \`skyvern.client.errors\`. The base \`ApiError\` class lives in \`skyvern.client.core\`.

 \*\*TypeScript:\*\* \`SkyvernError\` and \`SkyvernTimeoutError\` are top-level exports. The HTTP-specific errors (\`BadRequestError\`, etc.) extend \`SkyvernError\` and are accessed via the \`SkyvernApi\` namespace.

\\*\\*\\*

\## Catching errors

 \`\`\`python Python theme={null}
 from skyvern import Skyvern
 from skyvern.client.core import ApiError
 from skyvern.client.errors import NotFoundError

 client = Skyvern(api\_key="YOUR\_API\_KEY")

 try:
 run = await client.get\_run("tsk\_nonexistent")
 except NotFoundError as e:
 print(f"Run not found: {e.body}")
 except ApiError as e:
 print(f"API error {e.status\_code}: {e.body}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { Skyvern, SkyvernError, SkyvernApi } from "@skyvern/client";

 const skyvern = new Skyvern({ apiKey: "YOUR\_API\_KEY" });

 try {
 const run = await skyvern.getRun("tsk\_nonexistent");
 } catch (e) {
 if (e instanceof SkyvernApi.NotFoundError) {
 console.log(\`Run not found: ${e.body}\`);
 } else if (e instanceof SkyvernError) {
 console.log(\`API error ${e.statusCode}: ${e.body}\`);
 }
 }
 \`\`\`

\### Error properties

Every error has these attributes:

\| Property (Python) \| Property (TS) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`status\_code\` \| \`statusCode\` \| \`int \\\| None\` \| HTTP status code. \|
\| \`body\` \| \`body\` \| \`Any\` \| Response body (usually a dict with error details). \|
\| \`headers\` \| - \| \`dict\[str, str\] \\\| None\` \| Response headers. \|
\| \- \| \`rawResponse\` \| \`RawResponse \\\| undefined\` \| The raw HTTP response (TS only). \|
\| \- \| \`message\` \| \`string\` \| Human-readable error message (TS only). \|

\\*\\*\\*

\## Timeouts

Two different timeouts apply:

\### HTTP request timeout

Controls how long the SDK waits for the HTTP response from the Skyvern API. Set it in the constructor or per-request:

 \`\`\`python Python theme={null}
 # Global timeout (applies to all requests)
 client = Skyvern(api\_key="YOUR\_API\_KEY", timeout=30.0)

 # Per-request timeout
 from skyvern.client.core import RequestOptions

 result = await client.get\_run(
 "tsk\_abc123",
 request\_options=RequestOptions(timeout\_in\_seconds=10),
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Global timeout (applies to all requests)
 const skyvern = new Skyvern({
 apiKey: "YOUR\_API\_KEY",
 timeoutInSeconds: 30,
 });

 // Per-request timeout
 const result = await skyvern.getRun("tsk\_abc123", {
 timeoutInSeconds: 10,
 });
 \`\`\`

When an HTTP request times out in TypeScript, a \`SkyvernTimeoutError\` is thrown.

\### Completion timeout

Controls how long \`wait\_for\_completion\` / \`waitForCompletion\` polls before giving up. This is separate from the HTTP timeout:

 \`\`\`python Python theme={null}
 try:
 result = await client.run\_task(
 prompt="Extract data",
 url="https://example.com",
 wait\_for\_completion=True,
 timeout=300, # Give up after 5 minutes
 )
 except TimeoutError:
 print("Task didn't complete in time")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 try {
 const result = await skyvern.runTask({
 body: {
 prompt: "Extract data",
 url: "https://example.com",
 },
 waitForCompletion: true,
 timeout: 300, // Give up after 5 minutes
 });
 } catch (e) {
 if (e instanceof Error && e.message.includes("Timeout")) {
 console.log("Task didn't complete in time");
 }
 }
 \`\`\`

The completion timeout raises Python's built-in \`TimeoutError\` (via \`asyncio.timeout\`), not \`ApiError\`. In TypeScript, it throws a standard \`Error\` with a timeout message.

\\*\\*\\*

\## Retries

Configure automatic retries for transient failures. Set it in the constructor or per-request:

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 result = await client.run\_task(
 prompt="Extract product data",
 url="https://example.com/products",
 request\_options=RequestOptions(max\_retries=3),
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Global retries (default: 2)
 const skyvern = new Skyvern({
 apiKey: "YOUR\_API\_KEY",
 maxRetries: 3,
 });

 // Per-request retries
 const result = await skyvern.runTask(
 {
 body: {
 prompt: "Extract product data",
 url: "https://example.com/products",
 },
 },
 { maxRetries: 5 },
 );
 \`\`\`

Retries apply to the HTTP request level (network errors, 5xx responses). They do not retry the entire task if it fails at the AI level - use \`get\_run\` / \`getRun\` to check the status and re-run if needed.

\\*\\*\\*

\## Abort requests (TypeScript only)

Cancel in-flight requests using \`AbortSignal\`:

\`\`\`typescript theme={null}
const controller = new AbortController();

// Cancel after 10 seconds
setTimeout(() => controller.abort(), 10000);

try {
 const result = await skyvern.runTask(
 {
 body: {
 prompt: "Extract data",
 url: "https://example.com",
 },
 },
 { abortSignal: controller.signal },
 );
} catch (e) {
 if (e instanceof Error && e.name === "AbortError") {
 console.log("Request was aborted");
 }
}
\`\`\`

\\*\\*\\*

\## Run failure vs API errors

There are two distinct failure modes:

\*\*API error\*\* - The HTTP request itself failed. The SDK raises an exception.

 \`\`\`python Python theme={null}
 from skyvern.client.core import ApiError

 try:
 result = await client.run\_task(prompt="...")
 except ApiError as e:
 print(f"API call failed: {e.status\_code}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { SkyvernError } from "@skyvern/client";

 try {
 const result = await skyvern.runTask({
 body: { prompt: "..." },
 });
 } catch (e) {
 if (e instanceof SkyvernError) {
 console.log(\`API call failed: ${e.statusCode}\`);
 }
 }
 \`\`\`

\*\*Run failure\*\* - The API call succeeded, but the task/workflow failed during execution. No exception is raised. Check the \`status\` field:

 \`\`\`python Python theme={null}
 result = await client.run\_task(
 prompt="Fill out the form",
 url="https://example.com",
 wait\_for\_completion=True,
 )

 if result.status == "failed":
 print(f"Task failed: {result.failure\_reason}")
 elif result.status == "timed\_out":
 print(f"Task exceeded step limit after {result.step\_count} steps")
 elif result.status == "completed":
 print(f"Success: {result.output}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: "Fill out the form",
 url: "https://example.com",
 },
 waitForCompletion: true,
 });

 if (result.status === "failed") {
 console.log(\`Task failed: ${result.failure\_reason}\`);
 } else if (result.status === "timed\_out") {
 console.log(\`Task exceeded step limit after ${result.step\_count} steps\`);
 } else if (result.status === "completed") {
 console.log(\`Success: ${JSON.stringify(result.output)}\`);
 }
 \`\`\`

\### Run statuses

\| Status \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`created\` \| Run initialized, not yet queued. \|
\| \`queued\` \| Waiting for an available browser. \|
\| \`running\` \| AI is executing. \|
\| \`completed\` \| Finished successfully. \|
\| \`failed\` \| Encountered an error during execution. \|
\| \`terminated\` \| Manually stopped. \|
\| \`timed\_out\` \| Exceeded step limit (\`max\_steps\`). \|
\| \`canceled\` \| Canceled before starting. \|

---
## sdk-reference/tasks/run-task
Source: https://skyvern.com/docs/sdk-reference/tasks/run-task.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# run\_task

A task is a single browser automation. You describe what you want in natural language. Skyvern opens a browser, navigates to the URL, and executes the instructions with AI.

For when to use tasks vs workflows, see \[Run a Task\](/running-automations/run-a-task).

 Python uses \`snake\_case\` (e.g., \`run\_task\`, \`wait\_for\_completion\`); TypeScript uses \`camelCase\` (e.g., \`runTask\`, \`waitForCompletion\`) and wraps request params in a \`body\` object. Parameter tables show Python names. TypeScript names are the camelCase equivalents.

\\*\\*\\*

Start a browser automation. Skyvern opens a cloud browser, navigates to the URL, and executes your prompt with AI.

 \`\`\`python Python theme={null}
 result = await client.run\_task(
 prompt="Get the title of the top post",
 url="https://news.ycombinator.com",
 wait\_for\_completion=True,
 )
 print(result.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: "Get the title of the top post",
 url: "https://news.ycombinator.com",
 },
 waitForCompletion: true,
 });
 console.log(result.output);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`prompt\` \| \`str\` \| Yes \| - \| Natural language instructions for what the AI should do. \|
\| \`url\` \| \`str\` \| No \| \`None\` \| Starting page URL. If omitted, the AI navigates from a blank page. \|
\| \`engine\` \| \`RunEngine\` \| No \| \`skyvern\_v2\` \| AI engine. Options: \`skyvern\_v2\`, \`skyvern\_v1\`, \`openai\_cua\`, \`anthropic\_cua\`, \`ui\_tars\`. \|
\| \`wait\_for\_completion\` \| \`bool\` \| No \| \`False\` \| Block until the run finishes. \|
\| \`timeout\` \| \`float\` \| No \| \`1800\` \| Max wait time in seconds when \`wait\_for\_completion=True\`. \|
\| \`max\_steps\` \| \`int\` \| No \| \`None\` \| Cap the number of AI steps to limit cost. Run terminates with \`timed\_out\` if hit. \|
\| \`data\_extraction\_schema\` \| \`dict \\\| str\` \| No \| \`None\` \| JSON schema or Pydantic model name constraining the output shape. \|
\| \`proxy\_location\` \| \`ProxyLocation\` \| No \| \`None\` \| Route the browser through a geographic proxy. \|
\| \`browser\_session\_id\` \| \`str\` \| No \| \`None\` \| Run inside an existing \[browser session\](/developers/optimization/browser-sessions). \|
\| \`publish\_workflow\` \| \`bool\` \| No \| \`False\` \| Save the generated code as a reusable workflow. Only works with \`skyvern\_v2\`. \|
\| \`webhook\_url\` \| \`str\` \| No \| \`None\` \| URL to receive a POST when the run finishes. \|
\| \`error\_code\_mapping\` \| \`dict\[str, str\]\` \| No \| \`None\` \| Map custom error codes to failure reasons. \|
\| \`totp\_identifier\` \| \`str\` \| No \| \`None\` \| Identifier for TOTP verification. \|
\| \`totp\_url\` \| \`str\` \| No \| \`None\` \| URL to receive TOTP codes. \|
\| \`title\` \| \`str\` \| No \| \`None\` \| Display name for this run in the dashboard. \|
\| \`model\` \| \`dict\` \| No \| \`None\` \| Override the output model definition. \|
\| \`user\_agent\` \| \`str\` \| No \| \`None\` \| Custom User-Agent header for the browser. \|
\| \`extra\_http\_headers\` \| \`dict\[str, str\]\` \| No \| \`None\` \| Additional HTTP headers injected into every browser request. \|
\| \`include\_action\_history\_in\_verification\` \| \`bool\` \| No \| \`None\` \| Include action history when verifying task completion. \|
\| \`max\_screenshot\_scrolls\` \| \`int\` \| No \| \`None\` \| Number of scrolls for post-action screenshots. Useful for lazy-loaded content. \|
\| \`browser\_address\` \| \`str\` \| No \| \`None\` \| Connect to a browser at this CDP address instead of spinning up a new one. \|
\| \`run\_with\` \| \`str\` \| No \| \`None\` \| Force execution mode: \`"code"\` (use cached Playwright code) or \`"agent"\` (use AI). \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| - \| Per-request configuration (see below). \|

\### Returns \`TaskRunResponse\`

\| Field \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Unique identifier. Starts with \`tsk\_\` for task runs. \|
\| \`status\` \| \`str\` \| \`created\`, \`queued\`, \`running\`, \`completed\`, \`failed\`, \`terminated\`, \`timed\_out\`, or \`canceled\`. \|
\| \`output\` \| \`dict \\\| None\` \| Extracted data from the run. Shape depends on your prompt or \`data\_extraction\_schema\`. \|
\| \`downloaded\_files\` \| \`list\[FileInfo\] \\\| None\` \| Files downloaded during the run. \|
\| \`recording\_url\` \| \`str \\\| None\` \| URL to the session recording video. \|
\| \`screenshot\_urls\` \| \`list\[str\] \\\| None\` \| Final screenshots (most recent first). \|
\| \`failure\_reason\` \| \`str \\\| None\` \| Error description if the run failed. \|
\| \`app\_url\` \| \`str \\\| None\` \| Link to view this run in the Cloud UI. \|
\| \`step\_count\` \| \`int \\\| None\` \| Number of AI steps taken. \|
\| \`script\_run\` \| \`ScriptRunResponse \\\| None\` \| Code execution result if the run used generated code. \|
\| \`created\_at\` \| \`datetime\` \| When the run was created. \|
\| \`finished\_at\` \| \`datetime \\\| None\` \| When the run finished. \|

\### Examples

\*\*Extract structured data:\*\*

 \`\`\`python Python theme={null}
 result = await client.run\_task(
 prompt="Extract the name, price, and rating of the top 3 products",
 url="https://example.com/products",
 data\_extraction\_schema={
 "type": "array",
 "items": {
 "type": "object",
 "properties": {
 "name": {"type": "string"},
 "price": {"type": "string"},
 "rating": {"type": "number"},
 },
 },
 },
 wait\_for\_completion=True,
 )
 print(result.output)
 # \[{"name": "Widget A", "price": "$29.99", "rating": 4.5}, ...\]
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: "Extract the name, price, and rating of the top 3 products",
 url: "https://example.com/products",
 data\_extraction\_schema: {
 type: "array",
 items: {
 type: "object",
 properties: {
 name: { type: "string" },
 price: { type: "string" },
 rating: { type: "number" },
 },
 },
 },
 },
 waitForCompletion: true,
 });
 console.log(result.output);
 // \[{ name: "Widget A", price: "$29.99", rating: 4.5 }, ...\]
 \`\`\`

\*\*Run inside an existing browser session:\*\*

 \`\`\`python Python theme={null}
 session = await client.create\_browser\_session()

 result = await client.run\_task(
 prompt="Log in and download the latest invoice",
 url="https://app.example.com/login",
 browser\_session\_id=session.browser\_session\_id,
 wait\_for\_completion=True,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const session = await skyvern.createBrowserSession({});

 const result = await skyvern.runTask({
 body: {
 prompt: "Log in and download the latest invoice",
 url: "https://app.example.com/login",
 browser\_session\_id: session.browser\_session\_id,
 },
 waitForCompletion: true,
 });
 \`\`\`

\*\*Limit cost with max\\\_steps:\*\*

 \`\`\`python Python theme={null}
 result = await client.run\_task(
 prompt="Fill out the contact form",
 url="https://example.com/contact",
 max\_steps=10,
 wait\_for\_completion=True,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: "Fill out the contact form",
 url: "https://example.com/contact",
 max\_steps: 10,
 },
 waitForCompletion: true,
 });
 \`\`\`

\*\*Use a lighter engine:\*\*

 \`\`\`python Python theme={null}
 from skyvern.schemas.runs import RunEngine

 result = await client.run\_task(
 prompt="Get the page title",
 url="https://example.com",
 engine=RunEngine.skyvern\_v1,
 wait\_for\_completion=True,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: "Get the page title",
 url: "https://example.com",
 engine: "skyvern\_v1",
 },
 waitForCompletion: true,
 });
 \`\`\`

\*\*Publish as a reusable workflow:\*\*

 \`\`\`python Python theme={null}
 result = await client.run\_task(
 prompt="Fill out the contact form with the provided data",
 url="https://example.com/contact",
 publish\_workflow=True,
 wait\_for\_completion=True,
 )
 # The generated workflow is saved and can be re-triggered via run\_workflow
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runTask({
 body: {
 prompt: "Fill out the contact form with the provided data",
 url: "https://example.com/contact",
 publish\_workflow: true,
 },
 waitForCompletion: true,
 });
 // The generated workflow is saved and can be re-triggered via runWorkflow
 \`\`\`

\\*\\*\\*

\## Polling pattern

If you don't use \`wait\_for\_completion\` / \`waitForCompletion\`, poll \`get\_run\` / \`getRun\` manually:

 \`\`\`python Python theme={null}
 import asyncio

 task = await client.run\_task(
 prompt="Extract product data",
 url="https://example.com/products",
 )

 while True:
 run = await client.get\_run(task.run\_id)
 if run.status in ("completed", "failed", "terminated", "timed\_out", "canceled"):
 break
 await asyncio.sleep(5)

 print(run.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const task = await skyvern.runTask({
 body: {
 prompt: "Extract product data",
 url: "https://example.com/products",
 },
 });

 const terminalStatuses = \["completed", "failed", "terminated", "timed\_out", "canceled"\];
 let run;
 while (true) {
 run = await skyvern.getRun(task.run\_id);
 if (terminalStatuses.includes(run.status)) break;
 await new Promise((resolve) => setTimeout(resolve, 5000));
 }

 console.log(run.output);
 \`\`\`

 For production, prefer \`wait\_for\_completion=True\` / \`waitForCompletion: true\` or \[webhooks\](/developers/going-to-production/webhooks) over manual polling.

\\*\\*\\*

\## \`wait\_for\_completion\` / \`waitForCompletion\`

By default, \`run\_task\` / \`runTask\` and \`run\_workflow\` / \`runWorkflow\` return immediately after the run is queued. You get a \`run\_id\` and need to poll \`get\_run\` / \`getRun\` yourself. Pass \`wait\_for\_completion=True\` / \`waitForCompletion: true\` to have the SDK poll automatically until the run reaches a terminal state (\`completed\`, \`failed\`, \`terminated\`, \`timed\_out\`, or \`canceled\`):

 \`\`\`python Python theme={null}
 # Returns only after the task finishes (up to 30 min by default)
 result = await client.run\_task(
 prompt="Fill out the contact form",
 url="https://example.com/contact",
 wait\_for\_completion=True,
 timeout=600, # give up after 10 minutes
 )

 # Without wait\_for\_completion -- returns immediately
 task = await client.run\_task(
 prompt="Fill out the contact form",
 url="https://example.com/contact",
 )
 print(task.run\_id) # poll with client.get\_run(task.run\_id)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Returns only after the task finishes (up to 30 min by default)
 const result = await skyvern.runTask({
 body: {
 prompt: "Fill out the contact form",
 url: "https://example.com/contact",
 },
 waitForCompletion: true,
 timeout: 600, // give up after 10 minutes
 });

 // Without waitForCompletion -- returns immediately
 const task = await skyvern.runTask({
 body: {
 prompt: "Fill out the contact form",
 url: "https://example.com/contact",
 },
 });
 console.log(task.run\_id); // poll with skyvern.getRun(task.run\_id)
 \`\`\`

\| Parameter \| Type \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`wait\_for\_completion\` / \`waitForCompletion\` \| \`bool\` / \`boolean\` \| \`False\` / \`false\` \| Poll until the run finishes. \|
\| \`timeout\` \| \`float\` / \`number\` \| \`1800\` \| Maximum wait time in seconds. Raises \`TimeoutError\` (Python) or \`Error\` (TS) if exceeded. \|

Supported on \`run\_task\`/\`runTask\`, \`run\_workflow\`/\`runWorkflow\`, and \`login\`. In TypeScript, also supported on \`downloadFiles\`.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/get-run
Source: https://skyvern.com/docs/sdk-reference/tasks/get-run.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_run

Get the current status and results of any run (task or workflow).

 \`\`\`python Python theme={null}
 run = await client.get\_run("tsk\_v2\_486305187432193504")
 print(run.status, run.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const run = await skyvern.getRun("tsk\_v2\_486305187432193504");
 console.log(run.status, run.output);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Yes \| The run ID returned by \`run\_task\` or \`run\_workflow\`. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`GetRunResponse\`

A discriminated union based on \`run\_type\`. All variants share the same core fields as \`TaskRunResponse\` above, plus a \`run\_type\` field (\`task\_v1\`, \`task\_v2\`, \`openai\_cua\`, \`anthropic\_cua\`, \`ui\_tars\`, \`workflow\_run\`).

Workflow run responses additionally include \`run\_with\` and \`ai\_fallback\` fields.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/cancel-run
Source: https://skyvern.com/docs/sdk-reference/tasks/cancel-run.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# cancel\_run

Cancel a running or queued run.

 \`\`\`python Python theme={null}
 await client.cancel\_run("tsk\_v2\_486305187432193504")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.cancelRun("tsk\_v2\_486305187432193504");
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Yes \| The run ID to cancel. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

The run transitions to \`canceled\` status. If the run has already finished, this is a no-op.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/get-run-timeline
Source: https://skyvern.com/docs/sdk-reference/tasks/get-run-timeline.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_run\_timeline

Get the step-by-step timeline of a run. Each entry represents one AI action with screenshots and reasoning.

 \`\`\`python Python theme={null}
 timeline = await client.get\_run\_timeline("tsk\_v2\_486305187432193504")
 for step in timeline:
 print(f"Step {step.order}: {step.type} - {step.status}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const timeline = await skyvern.getRunTimeline("tsk\_v2\_486305187432193504");
 for (const step of timeline) {
 console.log(\`Step ${step.order}: ${step.type} - ${step.status}\`);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Yes \| The run ID. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`list\[WorkflowRunTimeline\]\`

Each timeline entry contains step details including type, status, order, and associated artifacts.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/get-run-artifacts
Source: https://skyvern.com/docs/sdk-reference/tasks/get-run-artifacts.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_run\_artifacts

Get all artifacts (screenshots, recordings, generated code, etc.) for a run.

 \`\`\`python Python theme={null}
 artifacts = await client.get\_run\_artifacts("tsk\_v2\_486305187432193504")
 for artifact in artifacts:
 print(f"{artifact.artifact\_type}: {artifact.uri}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const artifacts = await skyvern.getRunArtifacts("tsk\_v2\_486305187432193504");
 for (const artifact of artifacts) {
 console.log(\`${artifact.artifact\_type}: ${artifact.uri}\`);
 }
 \`\`\`

Filter by type to get specific artifacts:

 \`\`\`python Python theme={null}
 # Get only the generated Playwright scripts
 scripts = await client.get\_run\_artifacts(
 "tsk\_v2\_486305187432193504",
 artifact\_type=\["script\_file"\],
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const scripts = await skyvern.getRunArtifacts(
 "tsk\_v2\_486305187432193504",
 { artifact\_type: \["script\_file"\] },
 );
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Yes \| The run ID. \|
\| \`artifact\_type\` \| \`ArtifactType \\\| list\[ArtifactType\]\` \| No \| Filter by artifact type. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`list\[Artifact\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/get-artifact
Source: https://skyvern.com/docs/sdk-reference/tasks/get-artifact.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_artifact

Get a single artifact by ID.

 \`\`\`python Python theme={null}
 artifact = await client.get\_artifact("art\_abc123")
 print(artifact.uri)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const artifact = await skyvern.getArtifact("art\_abc123");
 console.log(artifact.uri);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`artifact\_id\` \| \`str\` \| Yes \| The artifact ID. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`Artifact\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/get-runs-v2
Source: https://skyvern.com/docs/sdk-reference/tasks/get-runs-v2.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_runs\_v2

List all runs across tasks and workflows for the current organization, with filtering and pagination.

 \`\`\`python Python theme={null}
 runs = await client.get\_runs\_v2(page=1, page\_size=20, status="completed")
 for run in runs:
 print(run.run\_id, run.status)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const runs = await skyvern.getRunsV2({ page: 1, page\_size: 20, status: "completed" });
 for (const run of runs) {
 console.log(run.run\_id, run.status);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`page\` \| \`int\` \| No \| Page number (1-indexed). \|
\| \`page\_size\` \| \`int\` \| No \| Results per page. \|
\| \`status\` \| \`RunStatus \\\| list\[RunStatus\]\` \| No \| Filter by run status. \|
\| \`search\_key\` \| \`str\` \| No \| Case-insensitive substring search (min 3 chars). \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`list\[TaskRunListItem\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/tasks/retry-run-webhook
Source: https://skyvern.com/docs/sdk-reference/tasks/retry-run-webhook.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# retry\_run\_webhook

Re-send the webhook notification for a completed run. Useful if your webhook endpoint was down when the run finished.

 \`\`\`python Python theme={null}
 await client.retry\_run\_webhook("tsk\_v2\_486305187432193504")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.retryRunWebhook("tsk\_v2\_486305187432193504");
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Yes \| The run ID. \|
\| \`webhook\_url\` \| \`str\` \| No \| Override the stored webhook URL for this retry. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/run-workflow
Source: https://skyvern.com/docs/sdk-reference/workflows/run-workflow.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# run\_workflow

A workflow chains multiple steps (blocks) into a single automation. Workflows support loops, conditionals, data passing between steps, and code-based re-execution.

For conceptual background, see \[Build a Workflow\](/cloud/building-workflows/build-a-workflow).

 Python uses \`snake\_case\` (e.g., \`run\_workflow\`); TypeScript uses \`camelCase\` (e.g., \`runWorkflow\`) and wraps request params in a \`body\` object. Parameter tables show Python names. TypeScript names are the camelCase equivalents.

Execute a workflow by its permanent ID. Skyvern opens a cloud browser and runs each block in sequence.

 \`\`\`python Python theme={null}
 result = await client.run\_workflow(
 workflow\_id="wpid\_abc123",
 wait\_for\_completion=True,
 )
 print(result.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runWorkflow({
 body: {
 workflow\_id: "wpid\_abc123",
 },
 waitForCompletion: true,
 });
 console.log(result.output);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_id\` \| \`str\` \| Yes \| - \| The workflow's permanent ID (\`wpid\_...\`). \|
\| \`parameters\` \| \`dict\` \| No \| \`None\` \| Input parameters defined in the workflow. Keys must match parameter names. \|
\| \`wait\_for\_completion\` \| \`bool\` \| No \| \`False\` \| Block until the workflow finishes. \|
\| \`timeout\` \| \`float\` \| No \| \`1800\` \| Max wait time in seconds when \`wait\_for\_completion=True\`. \|
\| \`run\_with\` \| \`str\` \| No \| \`None\` \| Force execution mode: \`"code"\` (use cached Playwright code) or \`"agent"\` (use AI). \|
\| \`ai\_fallback\` \| \`bool\` \| No \| \`None\` \| Fall back to AI if the cached code fails. \|
\| \`browser\_session\_id\` \| \`str\` \| No \| \`None\` \| Run inside an existing \[browser session\](/developers/optimization/browser-sessions). \|
\| \`browser\_profile\_id\` \| \`str\` \| No \| \`None\` \| Load a \[browser profile\](/developers/optimization/browser-profiles) (cookies, storage) into the session. \|
\| \`proxy\_location\` \| \`ProxyLocation\` \| No \| \`None\` \| Route the browser through a geographic proxy. \|
\| \`max\_steps\_override\` \| \`int\` \| No \| \`None\` \| Cap total AI steps across all blocks. \|
\| \`webhook\_url\` \| \`str\` \| No \| \`None\` \| URL to receive a POST when the run finishes. \|
\| \`title\` \| \`str\` \| No \| \`None\` \| Display name for this run in the dashboard. \|
\| \`totp\_identifier\` \| \`str\` \| No \| \`None\` \| Identifier for TOTP verification. \|
\| \`totp\_url\` \| \`str\` \| No \| \`None\` \| URL to receive TOTP codes. \|
\| \`template\` \| \`bool\` \| No \| \`None\` \| Run a template workflow. \|
\| \`user\_agent\` \| \`str\` \| No \| \`None\` \| Custom User-Agent header for the browser. \|
\| \`extra\_http\_headers\` \| \`dict\[str, str\]\` \| No \| \`None\` \| Additional HTTP headers injected into every browser request. \|
\| \`max\_screenshot\_scrolls\` \| \`int\` \| No \| \`None\` \| Number of scrolls for post-action screenshots. \|
\| \`browser\_address\` \| \`str\` \| No \| \`None\` \| Connect to a browser at this CDP address. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| - \| Per-request configuration (see below). \|

\### Returns \`WorkflowRunResponse\`

\| Field \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`run\_id\` \| \`str\` \| Unique identifier. Starts with \`wr\_\` for workflow runs. \|
\| \`status\` \| \`str\` \| \`created\`, \`queued\`, \`running\`, \`completed\`, \`failed\`, \`terminated\`, \`timed\_out\`, or \`canceled\`. \|
\| \`output\` \| \`dict \\\| None\` \| Extracted data from the workflow's output block. \|
\| \`downloaded\_files\` \| \`list\[FileInfo\] \\\| None\` \| Files downloaded during the run. \|
\| \`recording\_url\` \| \`str \\\| None\` \| URL to the session recording. \|
\| \`failure\_reason\` \| \`str \\\| None\` \| Error description if the run failed. \|
\| \`app\_url\` \| \`str \\\| None\` \| Link to view this run in the Cloud UI. \|
\| \`step\_count\` \| \`int \\\| None\` \| Total AI steps taken across all blocks. \|
\| \`run\_with\` \| \`str \\\| None\` \| Whether the run used \`"code"\` or \`"agent"\`. \|
\| \`ai\_fallback\` \| \`bool \\\| None\` \| Whether AI fallback was configured. \|
\| \`script\_run\` \| \`ScriptRunResponse \\\| None\` \| Code execution result. Contains \`ai\_fallback\_triggered\` if code was used. \|

\### Examples

\*\*Pass parameters to a workflow:\*\*

 \`\`\`python Python theme={null}
 result = await client.run\_workflow(
 workflow\_id="wpid\_invoice\_extraction",
 parameters={
 "company\_name": "Acme Corp",
 "date\_range": "2025-01-01 to 2025-12-31",
 },
 wait\_for\_completion=True,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runWorkflow({
 body: {
 workflow\_id: "wpid\_invoice\_extraction",
 parameters: {
 company\_name: "Acme Corp",
 date\_range: "2025-01-01 to 2025-12-31",
 },
 },
 waitForCompletion: true,
 });
 \`\`\`

\*\*Run with cached code (skip AI, use generated Playwright scripts):\*\*

\`\`\`python theme={null}
result = await client.run\_workflow(
 workflow\_id="wpid\_daily\_report",
 run\_with="code",
 ai\_fallback=True, # Fall back to AI if code fails
 wait\_for\_completion=True,
)
\`\`\`

\*\*Run with a browser profile (skip login):\*\*

 \`\`\`python Python theme={null}
 result = await client.run\_workflow(
 workflow\_id="wpid\_daily\_report",
 browser\_profile\_id="bpf\_abc123",
 wait\_for\_completion=True,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.runWorkflow({
 body: {
 workflow\_id: "wpid\_daily\_report",
 browser\_profile\_id: "bpf\_abc123",
 },
 waitForCompletion: true,
 });
 \`\`\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/create-workflow
Source: https://skyvern.com/docs/sdk-reference/workflows/create-workflow.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# create\_workflow

Create a new workflow from a JSON or YAML definition.

 \`\`\`python Python theme={null}
 workflow = await client.create\_workflow(
 json\_definition={
 "title": "Extract Products",
 "workflow\_definition": {
 "parameters": \[\
 {\
 "key": "target\_url",\
 "parameter\_type": "workflow",\
 "workflow\_parameter\_type": "string",\
 "description": "URL to scrape",\
 }\
 \],
 "blocks": \[\
 {\
 "block\_type": "task",\
 "label": "extract\_data",\
 "prompt": "Extract the top 3 products",\
 "url": "{{ target\_url }}",\
 }\
 \],
 },
 },
 )
 print(workflow.workflow\_permanent\_id)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const workflow = await skyvern.createWorkflow({
 body: {
 json\_definition: {
 title: "Extract Products",
 workflow\_definition: {
 parameters: \[\
 {\
 key: "target\_url",\
 parameter\_type: "workflow",\
 workflow\_parameter\_type: "string",\
 description: "URL to scrape",\
 },\
 \],
 blocks: \[\
 {\
 block\_type: "task",\
 label: "extract",\
 prompt: "Extract the top 3 products with name and price",\
 url: "{{ target\_url }}",\
 },\
 \],
 },
 },
 },
 });
 console.log(workflow.workflow\_permanent\_id);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`json\_definition\` \| \`WorkflowCreateYamlRequest\` \| No \| Workflow definition as a JSON object. \|
\| \`yaml\_definition\` \| \`str\` \| No \| Workflow definition as a YAML string. \|
\| \`folder\_id\` \| \`str\` \| No \| Folder to organize the workflow in. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

You must provide either \`json\_definition\` or \`yaml\_definition\`.

\### Returns \`Workflow\`

\| Field \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_id\` \| \`str\` \| Unique ID for this version. \|
\| \`workflow\_permanent\_id\` \| \`str\` \| Stable ID across all versions. Use this to run workflows. \|
\| \`version\` \| \`int\` \| Version number. \|
\| \`title\` \| \`str\` \| Workflow title. \|
\| \`workflow\_definition\` \| \`WorkflowDefinition\` \| The full definition including blocks and parameters. \|
\| \`status\` \| \`str \\\| None\` \| Workflow status. \|
\| \`created\_at\` \| \`datetime\` \| When the workflow was created. \|

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/get-workflow
Source: https://skyvern.com/docs/sdk-reference/workflows/get-workflow.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_workflow

 Python: requires \`skyvern\` version 1.1.0 or later. Run \`pip install --upgrade skyvern\` to update.

Get a specific workflow by its permanent ID.

 \`\`\`python Python theme={null}
 workflow = await client.get\_workflow("wpid\_abc123")
 print(workflow.title, f"v{workflow.version}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const workflow = await skyvern.getWorkflow("wpid\_abc123");
 console.log(workflow.title, \`v${workflow.version}\`);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_permanent\_id\` \| \`str\` \| Yes \| The workflow's permanent ID. \|
\| \`version\` \| \`int\` \| No \| Specific version to retrieve. Defaults to latest. \|
\| \`template\` \| \`bool\` \| No \| Whether to fetch a template workflow. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`Workflow\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/get-workflows
Source: https://skyvern.com/docs/sdk-reference/workflows/get-workflows.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_workflows

List all workflows. Supports filtering and pagination.

 \`\`\`python Python theme={null}
 workflows = await client.get\_workflows()
 for wf in workflows:
 print(f"{wf.title} ({wf.workflow\_permanent\_id})")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const workflows = await skyvern.getWorkflows({});
 for (const wf of workflows) {
 console.log(\`${wf.title} (${wf.workflow\_permanent\_id})\`);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`page\` \| \`int\` \| No \| \`None\` \| Page number for pagination. \|
\| \`page\_size\` \| \`int\` \| No \| \`None\` \| Number of results per page. \|
\| \`only\_saved\_tasks\` \| \`bool\` \| No \| \`None\` \| Only return saved tasks. \|
\| \`only\_workflows\` \| \`bool\` \| No \| \`None\` \| Only return workflows (not saved tasks). \|
\| \`only\_templates\` \| \`bool\` \| No \| \`None\` \| Only return templates. \|
\| \`template\` \| \`bool\` \| No \| \`None\` \| Only return template workflows. \|
\| \`title\` \| \`str\` \| No \| \`None\` \| Filter by title. Deprecated - use \`search\_key\` instead. \|
\| \`search\_key\` \| \`str\` \| No \| \`None\` \| Case-insensitive substring search across workflow title, folder name, and parameter metadata. \|
\| \`folder\_id\` \| \`str\` \| No \| \`None\` \| Filter by folder. \|
\| \`status\` \| \`WorkflowStatus \\\| list\[WorkflowStatus\]\` \| No \| \`None\` \| Filter by status. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| - \| Per-request configuration (see below). \|

\### Returns \`list\[Workflow\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/get-workflow-versions
Source: https://skyvern.com/docs/sdk-reference/workflows/get-workflow-versions.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_workflow\_versions

 Python: requires \`skyvern\` version 1.1.0 or later. Run \`pip install --upgrade skyvern\` to update.

List all versions of a workflow.

 \`\`\`python Python theme={null}
 versions = await client.get\_workflow\_versions("wpid\_abc123")
 for v in versions:
 print(f"v{v.version} - {v.modified\_at}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const versions = await skyvern.getWorkflowVersions("wpid\_abc123");
 for (const v of versions) {
 console.log(\`v${v.version} - ${v.modified\_at}\`);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_permanent\_id\` \| \`str\` \| Yes \| The workflow's permanent ID. \|
\| \`template\` \| \`bool\` \| No \| Whether to fetch template versions. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`list\[Workflow\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/update-workflow
Source: https://skyvern.com/docs/sdk-reference/workflows/update-workflow.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# update\_workflow

Update an existing workflow's definition.

 \`\`\`python Python theme={null}
 updated = await client.update\_workflow(
 "wpid\_abc123",
 json\_definition={
 "title": "Extract Products",
 "workflow\_definition": {
 "blocks": \[\
 {\
 "block\_type": "task",\
 "label": "extract\_data",\
 "prompt": "Extract the top 5 products",\
 "url": "https://example.com/products",\
 }\
 \],
 "parameters": \[\],
 },
 },
 )
 print(f"Updated to v{updated.version}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const updated = await skyvern.updateWorkflow("wpid\_abc123", {
 json\_definition: {
 title: "Extract Products Updated",
 workflow\_definition: {
 blocks: \[\
 {\
 block\_type: "task",\
 label: "extract\_data",\
 prompt: "Extract the top 5 products",\
 url: "https://example.com/products",\
 },\
 \],
 parameters: \[\],
 },
 },
 });
 console.log(\`Updated to v${updated.version}\`);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_id\` \| \`str\` \| Yes \| The workflow's permanent ID (\`wpid\_...\`). \|
\| \`json\_definition\` \| \`WorkflowCreateYamlRequest\` \| No \| Updated definition as a JSON object. \|
\| \`yaml\_definition\` \| \`str\` \| No \| Updated definition as a YAML string. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`Workflow\`

Creates a new version of the workflow.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/delete-workflow
Source: https://skyvern.com/docs/sdk-reference/workflows/delete-workflow.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# delete\_workflow

Delete a workflow.

 \`\`\`python Python theme={null}
 await client.delete\_workflow("wf\_abc123")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.deleteWorkflow("wf\_abc123");
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_id\` \| \`str\` \| Yes \| The workflow version ID to delete. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/get-workflow-runs
Source: https://skyvern.com/docs/sdk-reference/workflows/get-workflow-runs.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_workflow\_runs

List workflow runs across all workflows for the current organization. Results are paginated and can be filtered by status, search key, and error code.

 \`\`\`python Python theme={null}
 runs = await client.get\_workflow\_runs(page=1, page\_size=10)
 for run in runs:
 print(run.workflow\_run\_id, run.status)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const runs = await skyvern.getWorkflowRuns({ page: 1, page\_size: 10 });
 for (const run of runs) {
 console.log(run.workflow\_run\_id, run.status);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`page\` \| \`int\` \| No \| Page number (1-indexed). \|
\| \`page\_size\` \| \`int\` \| No \| Results per page. \|
\| \`status\` \| \`WorkflowRunStatus \\\| list\[WorkflowRunStatus\]\` \| No \| Filter by run status. \|
\| \`search\_key\` \| \`str\` \| No \| Case-insensitive substring search (min 3 chars). Matches against run ID, parameter keys, parameter values, and descriptions. \|
\| \`error\_code\` \| \`str\` \| No \| Filter by error code. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`list\[WorkflowRun\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/workflows/update-workflow-folder
Source: https://skyvern.com/docs/sdk-reference/workflows/update-workflow-folder.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# update\_workflow\_folder

Move a workflow to a different folder, or remove it from its current folder.

 \`\`\`python Python theme={null}
 workflow = await client.update\_workflow\_folder(
 "wpid\_abc123",
 folder\_id="folder\_456",
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const workflow = await skyvern.updateWorkflowFolder("wpid\_abc123", {
 folder\_id: "folder\_456",
 });
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_permanent\_id\` \| \`str\` \| Yes \| The workflow permanent ID. \|
\| \`folder\_id\` \| \`str\` \| No \| Folder ID to assign. Set to \`None\` / \`null\` to remove from folder. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`Workflow\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-sessions/create-browser-session
Source: https://skyvern.com/docs/sdk-reference/browser-sessions/create-browser-session.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# create\_browser\_session

A browser session is a persistent browser instance that stays alive between API calls. Use sessions to chain multiple tasks in the same browser without losing cookies, local storage, or login state.

For conceptual background, see \[Browser Sessions\](/developers/optimization/browser-sessions).

 Python uses \`snake\_case\` (e.g., \`create\_browser\_session\`); TypeScript uses \`camelCase\` (e.g., \`createBrowserSession\`). Parameter tables show Python names. TypeScript names are the camelCase equivalents.

Spin up a new cloud browser session.

 \`\`\`python Python theme={null}
 session = await client.create\_browser\_session(timeout=60)
 print(session.browser\_session\_id) # pbs\_abc123
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const session = await skyvern.createBrowserSession({ timeout: 60 });
 console.log(session.browser\_session\_id); // pbs\_abc123
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\` \| \`int\` \| No \| \`60\` \| Session timeout in minutes (5–1440). Timer starts after the session is ready. \|
\| \`proxy\_location\` \| \`ProxyLocation\` \| No \| \`None\` \| Route browser traffic through a geographic proxy. \|
\| \`extensions\` \| \`list\[Extensions\]\` \| No \| \`None\` \| Browser extensions to install. Options: \`"ad-blocker"\`, \`"captcha-solver"\`. \|
\| \`browser\_type\` \| \`PersistentBrowserType\` \| No \| \`None\` \| Browser type. Options: \`"chrome"\`, \`"msedge"\`. \|
\| \`browser\_profile\_id\` \| \`str\` \| No \| \`None\` \| Load a browser profile (cookies, localStorage) into this session. ID starts with \`bpf\_\`. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| \| Per-request configuration (see below). \|

\### Returns \`BrowserSessionResponse\`

\| Field \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`browser\_session\_id\` \| \`str\` \| Unique ID. Starts with \`pbs\_\`. \|
\| \`status\` \| \`str \\\| None\` \| Current session status. \|
\| \`browser\_address\` \| \`str \\\| None\` \| CDP address for connecting to the browser. \|
\| \`app\_url\` \| \`str \\\| None\` \| Link to the live browser view in the Cloud UI. \|
\| \`timeout\` \| \`int \\\| None\` \| Configured timeout in minutes. \|
\| \`started\_at\` \| \`datetime \\\| None\` \| When the session became ready. \|
\| \`created\_at\` \| \`datetime\` \| When the session was requested. \|

\### Example: Chain multiple tasks in one session

 \`\`\`python Python theme={null}
 session = await client.create\_browser\_session()

 # Step 1: Log in
 await client.run\_task(
 prompt="Log in with username demo@example.com",
 url="https://app.example.com/login",
 browser\_session\_id=session.browser\_session\_id,
 wait\_for\_completion=True,
 )

 # Step 2: Extract data (same browser, already logged in)
 result = await client.run\_task(
 prompt="Go to the invoices page and extract all invoice numbers",
 browser\_session\_id=session.browser\_session\_id,
 wait\_for\_completion=True,
 )
 print(result.output)

 # Clean up
 await client.close\_browser\_session(session.browser\_session\_id)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const session = await skyvern.createBrowserSession({});

 // Step 1: Log in
 await skyvern.runTask({
 body: {
 prompt: "Log in with username demo@example.com",
 url: "https://app.example.com/login",
 browser\_session\_id: session.browser\_session\_id,
 },
 waitForCompletion: true,
 });

 // Step 2: Extract data (same browser, already logged in)
 const result = await skyvern.runTask({
 body: {
 prompt: "Go to the invoices page and extract all invoice numbers",
 browser\_session\_id: session.browser\_session\_id,
 },
 waitForCompletion: true,
 });
 console.log(result.output);

 // Clean up
 await skyvern.closeBrowserSession(session.browser\_session\_id);
 \`\`\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-sessions/get-browser-session
Source: https://skyvern.com/docs/sdk-reference/browser-sessions/get-browser-session.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_browser\_session

Get the status and details of a session.

 \`\`\`python Python theme={null}
 session = await client.get\_browser\_session("pbs\_abc123")
 print(session.status, session.browser\_address)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const session = await skyvern.getBrowserSession("pbs\_abc123");
 console.log(session.status, session.browser\_address);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`browser\_session\_id\` \| \`str\` \| Yes \| The session ID. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`BrowserSessionResponse\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-sessions/get-browser-sessions
Source: https://skyvern.com/docs/sdk-reference/browser-sessions/get-browser-sessions.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_browser\_sessions

List all active browser sessions.

 \`\`\`python Python theme={null}
 sessions = await client.get\_browser\_sessions()
 for s in sessions:
 print(f"{s.browser\_session\_id} - {s.status}")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const sessions = await skyvern.getBrowserSessions();
 for (const s of sessions) {
 console.log(\`${s.browser\_session\_id} - ${s.status}\`);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`list\[BrowserSessionResponse\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-sessions/close-browser-session
Source: https://skyvern.com/docs/sdk-reference/browser-sessions/close-browser-session.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# close\_browser\_session

Close a browser session and release its resources.

 \`\`\`python Python theme={null}
 await client.close\_browser\_session("pbs\_abc123")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.closeBrowserSession("pbs\_abc123");
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`browser\_session\_id\` \| \`str\` \| Yes \| The session ID to close. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

 Closing a session is irreversible. Any unsaved state (cookies, local storage) is lost unless you created a \[browser profile\](/sdk-reference/browser-profiles) from it.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-profiles/create-browser-profile
Source: https://skyvern.com/docs/sdk-reference/browser-profiles/create-browser-profile.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# create\_browser\_profile

A browser profile is a snapshot of browser state: cookies, local storage, session data. Create a profile from a completed run, then load it into future workflow runs to skip login and setup steps.

For conceptual background, see \[Browser Profiles\](/developers/optimization/browser-profiles).

 Python uses \`snake\_case\` (e.g., \`create\_browser\_profile\`); TypeScript uses \`camelCase\` (e.g., \`createBrowserProfile\`). Parameter tables show Python names. TypeScript names are the camelCase equivalents.

Create a profile from a completed workflow run.

 \`\`\`python Python theme={null}
 profile = await client.create\_browser\_profile(
 name="production-login",
 workflow\_run\_id="wr\_abc123",
 )
 print(profile.browser\_profile\_id) # bpf\_abc123
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const profile = await skyvern.createBrowserProfile({
 name: "production-login",
 workflow\_run\_id: "wr\_abc123",
 });
 console.log(profile.browser\_profile\_id); // bpf\_abc123
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`name\` \| \`str\` \| Yes \| Display name for the profile. \|
\| \`description\` \| \`str\` \| No \| Optional description. \|
\| \`workflow\_run\_id\` \| \`str\` \| Conditional \| The workflow run ID to snapshot. The run must have used \`persist\_browser\_session=True\`. Required if \`browser\_session\_id\` is not provided. \|
\| \`browser\_session\_id\` \| \`str\` \| Conditional \| The browser session ID to snapshot. Required if \`workflow\_run\_id\` is not provided. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

You must provide either \`workflow\_run\_id\` or \`browser\_session\_id\`.

\### Returns \`BrowserProfile\`

\| Field \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`browser\_profile\_id\` \| \`str\` \| Unique ID. Starts with \`bpf\_\`. \|
\| \`name\` \| \`str\` \| Profile name. \|
\| \`description\` \| \`str \\\| None\` \| Profile description. \|
\| \`created\_at\` \| \`datetime\` \| When the profile was created. \|

\### Example: Create a profile from a login workflow

 \`\`\`python Python theme={null}
 # Step 1: Run a workflow with persist\_browser\_session
 run = await client.run\_workflow(
 workflow\_id="wpid\_login\_flow",
 parameters={"username": "demo@example.com"},
 wait\_for\_completion=True,
 )

 # Step 2: Create a profile from the run
 profile = await client.create\_browser\_profile(
 name="demo-account-login",
 workflow\_run\_id=run.run\_id,
 )

 # Step 3: Use the profile in future runs (skip login)
 result = await client.run\_workflow(
 workflow\_id="wpid\_extract\_invoices",
 browser\_profile\_id=profile.browser\_profile\_id,
 wait\_for\_completion=True,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Step 1: Run a workflow with persist\_browser\_session
 const run = await skyvern.runWorkflow({
 body: {
 workflow\_id: "wpid\_login\_flow",
 parameters: { username: "demo@example.com" },
 },
 waitForCompletion: true,
 });

 // Step 2: Create a profile from the run
 const profile = await skyvern.createBrowserProfile({
 name: "demo-account-login",
 workflow\_run\_id: run.run\_id,
 });

 // Step 3: Use the profile in future runs (skip login)
 const result = await skyvern.runWorkflow({
 body: {
 workflow\_id: "wpid\_extract\_invoices",
 browser\_profile\_id: profile.browser\_profile\_id,
 },
 waitForCompletion: true,
 });
 \`\`\`

 Session archiving is asynchronous. If \`create\_browser\_profile\` fails immediately after a workflow completes, wait a few seconds and retry.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-profiles/list-browser-profiles
Source: https://skyvern.com/docs/sdk-reference/browser-profiles/list-browser-profiles.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# list\_browser\_profiles

List all browser profiles.

 \`\`\`python Python theme={null}
 profiles = await client.list\_browser\_profiles()
 for p in profiles:
 print(f"{p.name} ({p.browser\_profile\_id})")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const profiles = await skyvern.listBrowserProfiles({});
 for (const p of profiles) {
 console.log(\`${p.name} (${p.browser\_profile\_id})\`);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`include\_deleted\` \| \`bool\` \| No \| \`None\` \| Include soft-deleted profiles in the results. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| \| Per-request configuration (see below). \|

\### Returns \`list\[BrowserProfile\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-profiles/get-browser-profile
Source: https://skyvern.com/docs/sdk-reference/browser-profiles/get-browser-profile.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_browser\_profile

Get a single profile by ID.

 \`\`\`python Python theme={null}
 profile = await client.get\_browser\_profile("bpf\_abc123")
 print(profile.name)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const profile = await skyvern.getBrowserProfile("bpf\_abc123");
 console.log(profile.name);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`profile\_id\` \| \`str\` \| Yes \| The browser profile ID. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`BrowserProfile\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-profiles/delete-browser-profile
Source: https://skyvern.com/docs/sdk-reference/browser-profiles/delete-browser-profile.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# delete\_browser\_profile

Delete a browser profile.

 \`\`\`python Python theme={null}
 await client.delete\_browser\_profile("bpf\_abc123")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.deleteBrowserProfile("bpf\_abc123");
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`profile\_id\` \| \`str\` \| Yes \| The browser profile ID to delete. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

 \`browser\_profile\_id\` only works with \`run\_workflow\`, not \`run\_task\`. If you pass it to \`run\_task\`, it will be silently ignored.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/credentials/create-credential
Source: https://skyvern.com/docs/sdk-reference/credentials/create-credential.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# create\_credential

Credentials let you store login information (username/password, TOTP secrets) securely in Skyvern's vault. Reference them by ID in tasks and workflows instead of passing secrets in your code.

 Python uses \`snake\_case\` (e.g., \`create\_credential\`); TypeScript uses \`camelCase\` (e.g., \`createCredential\`). Parameter tables show Python names. TypeScript names are the camelCase equivalents.

Store a new credential.

 \`\`\`python Python theme={null}
 credential = await client.create\_credential(
 name="my-app-login",
 credential\_type="password",
 credential={
 "username": "demo@example.com",
 "password": "s3cur3-p4ss",
 },
 )
 print(credential.credential\_id)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const credential = await skyvern.createCredential({
 name: "my-app-login",
 credential\_type: "password",
 credential: {
 username: "demo@example.com",
 password: "s3cur3-p4ss",
 },
 });
 console.log(credential.credential\_id);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`name\` \| \`str\` \| Yes \| Display name for the credential. \|
\| \`credential\_type\` \| \`CredentialType\` \| Yes \| Type of credential. \|
\| \`credential\` \| \`CreateCredentialRequestCredential\` \| Yes \| The credential data. Shape depends on \`credential\_type\`. \|
\| \`vault\_type\` \| \`CredentialVaultType\` \| No \| Which vault to store this credential in. If omitted, uses the default. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`CredentialResponse\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/credentials/get-credential
Source: https://skyvern.com/docs/sdk-reference/credentials/get-credential.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_credential

Get a single credential's metadata by ID.

 \`\`\`python Python theme={null}
 cred = await client.get\_credential("cred\_abc123")
 print(cred.name, cred.credential\_type)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const cred = await skyvern.getCredential("cred\_abc123");
 console.log(cred.name, cred.credential\_type);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`credential\_id\` \| \`str\` \| Yes \| The credential ID. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`CredentialResponse\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/credentials/get-credentials
Source: https://skyvern.com/docs/sdk-reference/credentials/get-credentials.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_credentials

List all credentials. Credential values are never returned - only metadata.

 \`\`\`python Python theme={null}
 creds = await client.get\_credentials()
 for c in creds:
 print(f"{c.name} ({c.credential\_id})")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const creds = await skyvern.getCredentials({});
 for (const c of creds) {
 console.log(\`${c.name} (${c.credential\_id})\`);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`page\` \| \`int\` \| No \| \`None\` \| Page number. \|
\| \`page\_size\` \| \`int\` \| No \| \`None\` \| Results per page. \|
\| \`vault\_type\` \| \`CredentialVaultType\` \| No \| \`None\` \| Filter credentials by vault type (e.g. \`"custom"\`, \`"bitwarden"\`, \`"azure\_vault"\`). \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| \`None\` \| Per-request configuration (see below). \|

\### Returns \`list\[CredentialResponse\]\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/credentials/update-credential
Source: https://skyvern.com/docs/sdk-reference/credentials/update-credential.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# update\_credential

Overwrite the stored credential data (e.g. username/password) while keeping the same credential ID.

 \`\`\`python Python theme={null}
 updated = await client.update\_credential(
 "cred\_abc123",
 name="Updated Login",
 credential\_type="password",
 credential={
 "username": "new\_user@example.com",
 "password": "new\_password",
 },
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const updated = await skyvern.updateCredential("cred\_abc123", {
 name: "Updated Login",
 credential\_type: "password",
 credential: {
 username: "new\_user@example.com",
 password: "new\_password",
 },
 });
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`credential\_id\` \| \`str\` \| Yes \| The credential ID to update. \|
\| \`name\` \| \`str\` \| Yes \| Name of the credential. \|
\| \`credential\_type\` \| \`str\` \| Yes \| Type of credential (\`"password"\`, \`"credit\_card"\`, \`"secret"\`). \|
\| \`credential\` \| \`dict\` \| Yes \| The new credential data. \|
\| \`vault\_type\` \| \`CredentialVaultType\` \| No \| Vault provider. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`CredentialResponse\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/credentials/delete-credential
Source: https://skyvern.com/docs/sdk-reference/credentials/delete-credential.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# delete\_credential

Delete a credential.

 \`\`\`python Python theme={null}
 await client.delete\_credential("cred\_abc123")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.deleteCredential("cred\_abc123");
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`credential\_id\` \| \`str\` \| Yes \| The credential ID to delete. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/credentials/send-totp-code
Source: https://skyvern.com/docs/sdk-reference/credentials/send-totp-code.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# send\_totp\_code

Send a TOTP (time-based one-time password) code to Skyvern during a run that requires 2FA. Call this when your webhook or polling detects that Skyvern is waiting for a TOTP code.

 \`\`\`python Python theme={null}
 await client.send\_totp\_code(
 totp\_identifier="demo@example.com",
 content="123456",
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await skyvern.sendTotpCode({
 totp\_identifier: "demo@example.com",
 content: "123456",
 });
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`totp\_identifier\` \| \`str\` \| Yes \| The identifier matching the \`totp\_identifier\` used in the task/workflow. \|
\| \`content\` \| \`str\` \| Yes \| The TOTP code value. \|
\| \`task\_id\` \| \`str\` \| No \| Associate with a specific task run. \|
\| \`workflow\_id\` \| \`str\` \| No \| Associate with a specific workflow. \|
\| \`workflow\_run\_id\` \| \`str\` \| No \| Associate with a specific workflow run. \|
\| \`source\` \| \`str\` \| No \| Source of the TOTP code. \|
\| \`expired\_at\` \| \`datetime\` \| No \| When this code expires. \|
\| \`type\` \| \`OtpType\` \| No \| OTP type. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`TotpCode\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/helpers/login
Source: https://skyvern.com/docs/sdk-reference/helpers/login.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# login

These methods wrap common multi-step patterns into single API calls. Under the hood, they create and run specialized workflows.

 Python uses \`snake\_case\` (e.g., \`login\`, \`download\_files\`); TypeScript uses \`camelCase\` (e.g., \`login\`, \`downloadFiles\`). Parameter tables show Python names. TypeScript names are the camelCase equivalents.

Automate logging into a website using stored credentials. This creates a login workflow, executes it, and optionally waits for completion.

 \`\`\`python Python theme={null}
 from skyvern.schemas.run\_blocks import CredentialType

 result = await client.login(
 credential\_type=CredentialType.skyvern,
 credential\_id="cred\_abc123",
 url="https://app.example.com/login",
 wait\_for\_completion=True,
 )
 print(result.status)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.login({
 credential\_type: "skyvern",
 credential\_id: "cred\_abc123",
 url: "https://app.example.com/login",
 waitForCompletion: true,
 });
 console.log(result.status);
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`credential\_type\` \| \`CredentialType\` \| Yes \| - \| How credentials are stored. Options: \`skyvern\`, \`bitwarden\`, \`onepassword\` (\`"1password"\` in TS), \`azure\_vault\`. \|
\| \`url\` \| \`str\` \| No \| \`None\` \| The login page URL. \|
\| \`credential\_id\` \| \`str\` \| No \| \`None\` \| The Skyvern credential ID (when using \`skyvern\` type). \|
\| \`prompt\` \| \`str\` \| No \| \`None\` \| Additional instructions for the AI during login. \|
\| \`browser\_session\_id\` \| \`str\` \| No \| \`None\` \| Run login inside an existing browser session. \|
\| \`browser\_address\` \| \`str\` \| No \| \`None\` \| Connect to a browser at this CDP address. \|
\| \`proxy\_location\` \| \`ProxyLocation\` \| No \| \`None\` \| Route browser traffic through a geographic proxy. \|
\| \`webhook\_url\` \| \`str\` \| No \| \`None\` \| URL to receive a POST when the login finishes. \|
\| \`totp\_identifier\` \| \`str\` \| No \| \`None\` \| Identifier for TOTP verification. \|
\| \`totp\_url\` \| \`str\` \| No \| \`None\` \| URL to receive TOTP codes. \|
\| \`wait\_for\_completion\` (Python) / \`waitForCompletion\` (TS) \| \`bool\` \| No \| \`False\` \| Block until the login finishes. \|
\| \`timeout\` \| \`float\` \| No \| \`1800\` \| Max wait time in seconds. \|
\| \`extra\_http\_headers\` \| \`dict\[str, str\]\` \| No \| \`None\` \| Additional HTTP headers. \|
\| \`max\_screenshot\_scrolling\_times\` \| \`int\` \| No \| \`None\` \| Number of screenshot scrolls. \|
\| \`browser\_profile\_id\` \| \`str\` \| No \| \`None\` \| Load a browser profile into the session. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| \`None\` \| Per-request configuration (see below). \|

\*\*Bitwarden-specific parameters:\*\*

\| Parameter \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`bitwarden\_collection\_id\` \| \`str\` \| Bitwarden collection ID. \|
\| \`bitwarden\_item\_id\` \| \`str\` \| Bitwarden item ID. \|

\*\*1Password-specific parameters:\*\*

\| Parameter \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`onepassword\_vault\_id\` \| \`str\` \| 1Password vault ID. \|
\| \`onepassword\_item\_id\` \| \`str\` \| 1Password item ID. \|

\*\*Azure Key Vault-specific parameters:\*\*

\| Parameter \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`azure\_vault\_name\` \| \`str\` \| Azure Key Vault name. \|
\| \`azure\_vault\_username\_key\` \| \`str\` \| Secret name for the username. \|
\| \`azure\_vault\_password\_key\` \| \`str\` \| Secret name for the password. \|
\| \`azure\_vault\_totp\_secret\_key\` \| \`str\` \| Secret name for the TOTP secret. \|

\### Returns \`WorkflowRunResponse\`

\### Example: Login then extract data

 \`\`\`python Python theme={null}
 from skyvern.schemas.run\_blocks import CredentialType

 session = await client.create\_browser\_session()

 # Login
 await client.login(
 credential\_type=CredentialType.skyvern,
 credential\_id="cred\_abc123",
 url="https://app.example.com/login",
 browser\_session\_id=session.browser\_session\_id,
 wait\_for\_completion=True,
 )

 # Now extract data from the authenticated session
 result = await client.run\_task(
 prompt="Go to the billing page and extract all invoices",
 browser\_session\_id=session.browser\_session\_id,
 wait\_for\_completion=True,
 )
 print(result.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const session = await skyvern.createBrowserSession({});

 // Login
 await skyvern.login({
 credential\_type: "skyvern",
 credential\_id: "cred\_abc123",
 url: "https://app.example.com/login",
 browser\_session\_id: session.browser\_session\_id,
 waitForCompletion: true,
 });

 // Now extract data from the authenticated session
 const result = await skyvern.runTask({
 body: {
 prompt: "Go to the billing page and extract all invoices",
 browser\_session\_id: session.browser\_session\_id,
 },
 waitForCompletion: true,
 });
 console.log(result.output);
 \`\`\`

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/helpers/download-files
Source: https://skyvern.com/docs/sdk-reference/helpers/download-files.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# download\_files

Navigate to a page and download files.

 Python's \`download\_files\` does \*\*not\*\* support \`wait\_for\_completion\` - it returns immediately with a \`run\_id\`. Poll with \`get\_run()\` or use a webhook to know when the download finishes. The TypeScript SDK \*\*does\*\* support \`waitForCompletion\` on \`downloadFiles\`.

 \`\`\`python Python theme={null}
 result = await client.download\_files(
 navigation\_goal="Download the latest monthly report PDF",
 url="https://app.example.com/reports",
 )

 # Poll for completion
 import asyncio
 while True:
 run = await client.get\_run(result.run\_id)
 if run.status in ("completed", "failed", "terminated", "timed\_out", "canceled"):
 break
 await asyncio.sleep(5)

 for f in run.downloaded\_files:
 print(f.name)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await skyvern.downloadFiles({
 navigation\_goal: "Download the latest monthly report PDF",
 url: "https://app.example.com/reports",
 waitForCompletion: true,
 });

 for (const f of result.downloaded\_files ?? \[\]) {
 console.log(f.name);
 }
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`navigation\_goal\` \| \`str\` \| Yes \| - \| Natural language description of what to download. \|
\| \`url\` \| \`str\` \| No \| \`None\` \| Starting page URL. \|
\| \`browser\_session\_id\` \| \`str\` \| No \| \`None\` \| Run inside an existing browser session. \|
\| \`browser\_profile\_id\` \| \`str\` \| No \| \`None\` \| Load a browser profile. \|
\| \`proxy\_location\` \| \`ProxyLocation\` \| No \| \`None\` \| Route through a geographic proxy. \|
\| \`webhook\_url\` \| \`str\` \| No \| \`None\` \| URL to receive a POST when the download finishes. \|
\| \`download\_suffix\` \| \`str\` \| No \| \`None\` \| Expected file extension to wait for (e.g., \`".pdf"\`). \|
\| \`download\_timeout\` \| \`float\` \| No \| \`None\` \| Max time to wait for the download in seconds. \|
\| \`max\_steps\_per\_run\` \| \`int\` \| No \| \`None\` \| Cap AI steps. \|
\| \`extra\_http\_headers\` \| \`dict\[str, str\]\` \| No \| \`None\` \| Additional HTTP headers. \|
\| \`totp\_identifier\` \| \`str\` \| No \| \`None\` \| Identifier for TOTP verification. \|
\| \`totp\_url\` \| \`str\` \| No \| \`None\` \| URL to receive TOTP codes. \|
\| \`browser\_address\` \| \`str\` \| No \| \`None\` \| Connect to a browser at this CDP address. \|
\| \`max\_screenshot\_scrolling\_times\` \| \`int\` \| No \| \`None\` \| Number of screenshot scrolls. \|
\| \`waitForCompletion\` (TS only) \| \`boolean\` \| No \| \`false\` \| Block until the download finishes. \|
\| \`timeout\` (TS only) \| \`number\` \| No \| \`1800\` \| Max wait time in seconds. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| \`None\` \| Per-request configuration (see below). \|

\### Returns \`WorkflowRunResponse\`

The \`downloaded\_files\` field contains the list of files that were downloaded.

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/helpers/upload-file
Source: https://skyvern.com/docs/sdk-reference/helpers/upload-file.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# upload\_file

Upload a file to Skyvern's storage. Returns a presigned URL and S3 URI you can reference in tasks and workflows.

 \`\`\`python Python theme={null}
 with open("data.csv", "rb") as f:
 upload = await client.upload\_file(file=f)
 print(upload.s3uri) # s3://skyvern-uploads/...
 print(upload.presigned\_url) # https://...signed download URL
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import fs from "fs";

 const upload = await skyvern.uploadFile({
 file: fs.createReadStream("data.csv"),
 });
 console.log(upload.s3\_uri); // s3://skyvern-uploads/...
 console.log(upload.presigned\_url); // https://...signed download URL
 \`\`\`

\### Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`file\` \| \`File\` (Python) / \`File \\\| ReadStream \\\| Blob\` (TS) \| Yes \| The file to upload. \|
\| \`request\_options\` \| \`RequestOptions\` \| No \| Per-request configuration (see below). \|

\### Returns \`UploadFileResponse\`

\| Field \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`s3uri\` (Python) / \`s3\_uri\` (TS) \| \`str\` \| S3 URI for the uploaded file. \|
\| \`presigned\_url\` \| \`str\` \| Pre-signed download URL. \|

\\*\\*\\*

\### Request options

Override timeout, retries, or headers for this call by passing \`request\_options\` (Python) or a second options argument (TypeScript).

 \`\`\`python Python theme={null}
 from skyvern.client.core import RequestOptions

 request\_options=RequestOptions(
 timeout\_in\_seconds=120,
 max\_retries=3,
 additional\_headers={"x-custom-header": "value"},
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Pass as second argument to any method
 {
 timeoutInSeconds: 120,
 maxRetries: 3,
 headers: { "x-custom-header": "value" },
 }
 \`\`\`

\| Option (Python) \| Option (TypeScript) \| Type \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\_in\_seconds\` \| \`timeoutInSeconds\` \| \`int\` / \`number\` \| HTTP timeout in seconds. \|
\| \`max\_retries\` \| \`maxRetries\` \| \`int\` / \`number\` \| Retry count. \|
\| \`additional\_headers\` \| \`headers\` \| \`dict\` / \`Record\` \| Extra headers. \|
\| \`additional\_query\_parameters\` \| - \| \`dict\` \| Extra query parameters. \|
\| \`additional\_body\_parameters\` \| - \| \`dict\` \| Extra body parameters. \|
\| \- \| \`abortSignal\` \| \`AbortSignal\` \| Signal to cancel the request. \|
\| \- \| \`apiKey\` \| \`string\` \| Override API key. \|

\\*\\*\\*

---
## sdk-reference/browser-automation/use-cloud-browser
Source: https://skyvern.com/docs/sdk-reference/browser-automation/use-cloud-browser.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# use\_cloud\_browser

Get or create a cloud browser session. Reuses the most recent available session if one exists, otherwise creates a new one.

 \`\`\`python Python theme={null}
 browser = await skyvern.use\_cloud\_browser()
 page = await browser.get\_working\_page()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const browser = await skyvern.useCloudBrowser();
 const page = await browser.getWorkingPage();
 \`\`\`

\## Parameters

Same parameters as \`launch\_cloud\_browser\` / \`launchCloudBrowser\`. Options are only used when creating a new session.

\| Parameter (Python) \| Parameter (TS) \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\` \| \`timeout\` \| \`int\` / \`number\` \| No \| \`60\` \| Session timeout in minutes (5--1440). \|
\| \`proxy\_location\` \| \`proxyLocation\` \| \`ProxyLocation\` \| No \| \`None\` / \`undefined\` \| Geographic proxy location for browser traffic. \|

\## Returns \`SkyvernBrowser\`

---
## sdk-reference/browser-automation/connect-to-cloud-browser-session
Source: https://skyvern.com/docs/sdk-reference/browser-automation/connect-to-cloud-browser-session.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# connect\_to\_cloud\_browser\_session

Connect to an existing cloud browser session by ID.

 \`\`\`python Python theme={null}
 browser = await skyvern.connect\_to\_cloud\_browser\_session("pbs\_abc123")
 page = await browser.get\_working\_page()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const browser = await skyvern.connectToCloudBrowserSession("pbs\_abc123");
 const page = await browser.getWorkingPage();
 \`\`\`

\## Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`browser\_session\_id\` / \`browserSessionId\` \| \`str\` / \`string\` \| Yes \| The ID of the cloud browser session. \|

\## Returns \`SkyvernBrowser\`

---
## sdk-reference/browser-automation/connect-to-browser-over-cdp
Source: https://skyvern.com/docs/sdk-reference/browser-automation/connect-to-browser-over-cdp.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# connect\_to\_browser\_over\_cdp

Connect to any browser running with Chrome DevTools Protocol (CDP) enabled, whether local or remote.

 \`\`\`python Python theme={null}
 browser = await skyvern.connect\_to\_browser\_over\_cdp("http://localhost:9222")
 page = await browser.get\_working\_page()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const browser = await skyvern.connectToBrowserOverCdp("http://localhost:9222");
 const page = await browser.getWorkingPage();
 \`\`\`

\## Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`cdp\_url\` / \`cdpUrl\` \| \`str\` / \`string\` \| Yes \| The CDP WebSocket URL (e.g., \`"http://localhost:9222"\`). \|

\## Returns \`SkyvernBrowser\`

---
## sdk-reference/browser-automation/launch-local-browser
Source: https://skyvern.com/docs/sdk-reference/browser-automation/launch-local-browser.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# launch\_local\_browser

Launch a local Chromium browser with CDP enabled. Only available in embedded mode (\`Skyvern.local()\`).

\`\`\`python theme={null}
skyvern = Skyvern.local()
browser = await skyvern.launch\_local\_browser(headless=False)
page = await browser.get\_working\_page()
\`\`\`

\## Parameters

\| Parameter \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`headless\` \| \`bool\` \| No \| \`False\` \| Run browser without a visible window. \|
\| \`port\` \| \`int\` \| No \| \`9222\` \| CDP port. \|
\| \`args\` \| \`list\[str\]\` \| No \| \`None\` \| Additional Chromium launch arguments. \|
\| \`user\_data\_dir\` \| \`str\` \| No \| \`None\` \| Custom user data directory for the browser. \|

\## Returns \`SkyvernBrowser\`

 \`launch\_local\_browser\` only works in embedded mode because a remote server cannot reach localhost. TypeScript SDK does not support local mode.

---
## sdk-reference/browser-automation/launch-cloud-browser
Source: https://skyvern.com/docs/sdk-reference/browser-automation/launch-cloud-browser.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# launch\_cloud\_browser

Create a new cloud browser session and connect to it. Returns a \`SkyvernBrowser\` with a live Playwright context.

 Python uses \`snake\_case\` (e.g., \`launch\_cloud\_browser\`, \`get\_working\_page\`); TypeScript uses \`camelCase\` (e.g., \`launchCloudBrowser\`, \`getWorkingPage\`). Some features - form automation, iframe management, \`AILocator\`, and local browser launch - are Python-only and clearly marked below.

\\*\\*\\*

 \`\`\`python Python theme={null}
 browser = await skyvern.launch\_cloud\_browser()
 page = await browser.get\_working\_page()

 await page.goto("https://example.com")
 await page.agent.run\_task("Fill out the contact form and submit it")

 await browser.close()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const browser = await skyvern.launchCloudBrowser();
 const page = await browser.getWorkingPage();

 await page.goto("https://example.com");
 await page.agent.runTask("Fill out the contact form and submit it");

 await browser.close();
 \`\`\`

\## Parameters

\| Parameter (Python) \| Parameter (TS) \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`timeout\` \| \`timeout\` \| \`int\` / \`number\` \| No \| \`60\` \| Session timeout in minutes (5–1440). \|
\| \`proxy\_location\` \| \`proxyLocation\` \| \`ProxyLocation\` \| No \| \`None\` / \`undefined\` \| Geographic proxy location for browser traffic. \|

\## Returns \`SkyvernBrowser\`

 Cloud browser sessions are only available with \`SkyvernEnvironment.CLOUD\` / \`.Cloud\` or \`SkyvernEnvironment.STAGING\` / \`.Staging\`.

---
## sdk-reference/browser-automation/get-working-page
Source: https://skyvern.com/docs/sdk-reference/browser-automation/get-working-page.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_working\_page

Get the most recent page or create a new one if none exists.

 \`\`\`python Python theme={null}
 page = await browser.get\_working\_page()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const page = await browser.getWorkingPage();
 \`\`\`

Returns a \`SkyvernBrowserPage\` - a Playwright \`Page\` with AI methods added.

---
## sdk-reference/browser-automation/new-page
Source: https://skyvern.com/docs/sdk-reference/browser-automation/new-page.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# new\_page

Create a new page (tab) in the browser context.

 \`\`\`python Python theme={null}
 page = await browser.new\_page()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const page = await browser.newPage();
 \`\`\`

Returns a \`SkyvernBrowserPage\` - a Playwright \`Page\` with AI methods added.

---
## sdk-reference/browser-automation/get-page-for
Source: https://skyvern.com/docs/sdk-reference/browser-automation/get-page-for.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# get\_page\_for

Wrap an existing Playwright \`Page\` with Skyvern AI capabilities.

\`\`\`python theme={null}
skyvern\_page = await browser.get\_page\_for(existing\_playwright\_page)
\`\`\`

\## Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`page\` \| \`Page\` \| Yes \| An existing Playwright \`Page\` object to wrap. \|

\## Returns \`SkyvernBrowserPage\`

---
## sdk-reference/browser-automation/close
Source: https://skyvern.com/docs/sdk-reference/browser-automation/close.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# close

Close the browser and release resources. If connected to a cloud session, also closes the session.

 \`\`\`python Python theme={null}
 await browser.close()
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await browser.close();
 \`\`\`

\## Returns \`None\`

---
## sdk-reference/browser-automation/complete-example
Source: https://skyvern.com/docs/sdk-reference/browser-automation/complete-example.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Complete Example

 \`\`\`python Python theme={null}
 import asyncio
 from skyvern import Skyvern

 async def main():
 skyvern = Skyvern(api\_key="YOUR\_API\_KEY")
 browser = await skyvern.launch\_cloud\_browser()
 page = await browser.get\_working\_page()

 # Navigate with Playwright
 await page.goto("https://app.example.com")

 # Login with AI
 await page.agent.login(
 credential\_type="skyvern",
 credential\_id="cred\_abc123",
 )

 # Mix Playwright and AI
 await page.click("#billing-tab")
 data = await page.extract(
 "Extract all invoice numbers and amounts",
 schema={
 "type": "array",
 "items": {
 "type": "object",
 "properties": {
 "invoice\_number": {"type": "string"},
 "amount": {"type": "string"},
 },
 },
 },
 )
 print(data)

 await browser.close()

 asyncio.run(main())
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 import { Skyvern } from "@skyvern/client";

 const skyvern = new Skyvern({ apiKey: "YOUR\_API\_KEY" });
 const browser = await skyvern.launchCloudBrowser();
 const page = await browser.getWorkingPage();

 // Navigate with Playwright
 await page.goto("https://app.example.com");

 // Login with AI
 await page.agent.login("skyvern", { credentialId: "cred\_abc123" });

 // Extract data with AI
 const data = await page.extract({
 prompt: "Extract all invoice numbers and amounts from the billing page",
 schema: {
 type: "array",
 items: {
 type: "object",
 properties: {
 invoice\_number: { type: "string" },
 amount: { type: "string" },
 },
 },
 },
 });
 console.log(data);

 // Clean up
 await browser.close();
 \`\`\`

---
## sdk-reference/browser-automation/act
Source: https://skyvern.com/docs/sdk-reference/browser-automation/act.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# act

Perform a freeform AI action on the page. The AI agent interprets the prompt, identifies the relevant elements, and executes the appropriate browser actions.

 \`\`\`python Python theme={null}
 await page.act("Scroll down and click the 'Load More' button")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 await page.act("Scroll down and click the 'Load More' button");
 \`\`\`

\`\`\`python theme={null}
await page.act("Click the login button")
await page.act("Select 'United States' from the country dropdown")
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`prompt\` \| \`str\` / \`string\` \| Yes \| Natural language instruction describing the action to perform. \|
\| \`skip\_refresh\` / \`skipRefresh\` \| \`bool\` / \`boolean\` \| No \| Skip refreshing the page state before acting. Defaults to \`False\`. \|
\| \`use\_economy\_tree\` / \`useEconomyTree\` \| \`bool\` / \`boolean\` \| No \| Use a lighter DOM representation to reduce token usage. Defaults to \`False\`. \|

Returns \`None\` / \`void\`.

---
## sdk-reference/browser-automation/agent-run-task
Source: https://skyvern.com/docs/sdk-reference/browser-automation/agent-run-task.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# agent.run\_task

Run a complete AI task in the context of the current page.

 \`\`\`python Python theme={null}
 result = await page.agent.run\_task(
 "Fill out the contact form and submit it",
 data\_extraction\_schema={
 "type": "object",
 "properties": {
 "confirmation\_number": {"type": "string"},
 },
 },
 )
 print(result.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await page.agent.runTask("Fill out the contact form and submit it", {
 dataExtractionSchema: {
 type: "object",
 properties: {
 confirmation\_number: { type: "string" },
 },
 },
 });
 console.log(result.output);
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`prompt\` \| \`str\` / \`string\` \| Yes \| Natural language task description. \|
\| \`engine\` \| \`RunEngine\` \| No \| AI engine to use. Default: \`skyvern\_v1\`. \|
\| \`model\` \| \`dict\` / \`Record\` \| No \| LLM model configuration. \|
\| \`url\` \| \`str\` / \`string\` \| No \| URL to navigate to. Defaults to current page URL. \|
\| \`data\_extraction\_schema\` / \`dataExtractionSchema\` \| \`dict \\\| str\` \| No \| JSON schema for output. \|
\| \`max\_steps\` / \`maxSteps\` \| \`int\` / \`number\` \| No \| Maximum AI steps. \|
\| \`timeout\` \| \`float\` / \`number\` \| No \| Max wait time in seconds. Default: \`1800\`. \|
\| \`webhook\_url\` / \`webhookUrl\` \| \`str\` / \`string\` \| No \| Webhook URL for notifications. \|
\| \`totp\_identifier\` / \`totpIdentifier\` \| \`str\` / \`string\` \| No \| TOTP identifier. \|
\| \`totp\_url\` / \`totpUrl\` \| \`str\` / \`string\` \| No \| TOTP URL. \|
\| \`title\` \| \`str\` / \`string\` \| No \| Run display name. \|
\| \`user\_agent\` \| \`str\` / \`string\` \| No \| Custom User-Agent header for the browser. \|
\| \`error\_code\_mapping\` / \`errorCodeMapping\` \| \`dict\` / \`Record\` \| No \| Custom error code mapping. \|

Returns \`TaskRunResponse\`.

---
## sdk-reference/browser-automation/agent-run-workflow
Source: https://skyvern.com/docs/sdk-reference/browser-automation/agent-run-workflow.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# agent.run\_workflow

Run a pre-defined workflow in the context of the current page.

 \`\`\`python Python theme={null}
 result = await page.agent.run\_workflow(
 "wpid\_abc123",
 parameters={"company\_name": "Acme Corp"},
 )
 print(result.output)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await page.agent.runWorkflow("wpid\_abc123", {
 parameters: { company\_name: "Acme Corp" },
 });
 console.log(result.output);
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`workflow\_id\` / \`workflowId\` \| \`str\` / \`string\` \| Yes \| The workflow permanent ID. \|
\| \`parameters\` \| \`dict\` / \`Record\` \| No \| Workflow input parameters. \|
\| \`template\` \| \`bool\` / \`boolean\` \| No \| Whether it's a template. \|
\| \`title\` \| \`str\` / \`string\` \| No \| Run display name. \|
\| \`timeout\` \| \`float\` / \`number\` \| No \| Max wait time in seconds. Default: \`1800\`. \|

Returns \`WorkflowRunResponse\`.

---
## sdk-reference/browser-automation/agent-login
Source: https://skyvern.com/docs/sdk-reference/browser-automation/agent-login.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# agent.login

Run a login workflow in the context of the current page. Supports multiple credential providers.

\## Parameters

\| Parameter (Python) \| Parameter (TS) \| Type \| Required \| Default \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`credential\_type\` \| first positional arg \| \`CredentialType\` / \`string\` \| Yes \| - \| Provider type: \`skyvern\`, \`bitwarden\`, \`onepassword\`, \`azure\_vault\`. \|
\| \`url\` \| \`url\` \| \`str\` / \`string\` \| No \| \`None\` / \`undefined\` \| URL to navigate to before logging in. \|
\| \`credential\_id\` \| \`credentialId\` \| \`str\` / \`string\` \| No \| \`None\` / \`undefined\` \| Skyvern credential ID. Required when \`credential\_type\` is \`skyvern\`. \|
\| \`prompt\` \| \`prompt\` \| \`str\` / \`string\` \| No \| \`None\` / \`undefined\` \| Additional natural-language login instructions. \|
\| \`webhook\_url\` \| \`webhookUrl\` \| \`str\` / \`string\` \| No \| \`None\` / \`undefined\` \| URL to receive a callback when login completes. \|
\| \`totp\_identifier\` \| \`totpIdentifier\` \| \`str\` / \`string\` \| No \| \`None\` / \`undefined\` \| Identifier for TOTP-based two-factor authentication. \|
\| \`totp\_url\` \| \`totpUrl\` \| \`str\` / \`string\` \| No \| \`None\` / \`undefined\` \| URL for TOTP secret retrieval. \|
\| \`extra\_http\_headers\` \| \`extraHttpHeaders\` \| \`dict\` / \`object\` \| No \| \`None\` / \`undefined\` \| Additional HTTP headers to set on the browser context. \|
\| \`timeout\` \| \`timeout\` \| \`float\` / \`number\` \| No \| \`1800\` \| Maximum time in seconds to wait for login to complete. \|

 Provider-specific parameters (\`bitwarden\_item\_id\`, \`onepassword\_vault\_id\`, etc.) are required based on the \`credential\_type\` chosen. See the examples below for each provider.

\## Examples

 \`\`\`python Python theme={null}
 from skyvern.schemas.run\_blocks import CredentialType

 # Skyvern credentials
 await page.agent.login(
 credential\_type=CredentialType.skyvern,
 credential\_id="cred\_123",
 )

 # Bitwarden
 await page.agent.login(
 credential\_type=CredentialType.bitwarden,
 bitwarden\_item\_id="item\_id",
 bitwarden\_collection\_id="collection\_id",
 )

 # 1Password
 await page.agent.login(
 credential\_type=CredentialType.onepassword,
 onepassword\_vault\_id="vault\_id",
 onepassword\_item\_id="item\_id",
 )

 # Azure Vault
 await page.agent.login(
 credential\_type=CredentialType.azure\_vault,
 azure\_vault\_name="vault\_name",
 azure\_vault\_username\_key="username\_key",
 azure\_vault\_password\_key="password\_key",
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Skyvern credentials
 await page.agent.login("skyvern", {
 credentialId: "cred\_123",
 });

 // Bitwarden
 await page.agent.login("bitwarden", {
 bitwardenItemId: "item\_id",
 bitwardenCollectionId: "collection\_id",
 });

 // 1Password
 await page.agent.login("1password", {
 onepasswordVaultId: "vault\_id",
 onepasswordItemId: "item\_id",
 });

 // Azure Vault
 await page.agent.login("azure\_vault", {
 azureVaultName: "vault\_name",
 azureVaultUsernameKey: "username\_key",
 azureVaultPasswordKey: "password\_key",
 });
 \`\`\`

Returns \`WorkflowRunResponse\`.

---
## sdk-reference/browser-automation/agent-download-files
Source: https://skyvern.com/docs/sdk-reference/browser-automation/agent-download-files.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# agent.download\_files

Download files in the context of the current page.

 \`\`\`python Python theme={null}
 result = await page.agent.download\_files(
 "Download the latest invoice PDF",
 download\_suffix=".pdf",
 download\_timeout=30,
 )
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await page.agent.downloadFiles("Download the latest invoice PDF", {
 downloadSuffix: ".pdf",
 downloadTimeout: 30,
 });
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`prompt\` \| \`str\` / \`string\` \| Yes \| What to download. \|
\| \`url\` \| \`str\` / \`string\` \| No \| URL to navigate to. Defaults to current page URL. \|
\| \`download\_suffix\` / \`downloadSuffix\` \| \`str\` / \`string\` \| No \| Expected file extension. \|
\| \`download\_timeout\` / \`downloadTimeout\` \| \`float\` / \`number\` \| No \| Download timeout in seconds. \|
\| \`max\_steps\_per\_run\` / \`maxStepsPerRun\` \| \`int\` / \`number\` \| No \| Max AI steps. \|
\| \`timeout\` \| \`float\` / \`number\` \| No \| Max wait time in seconds. Default: \`1800\`. \|

Returns \`WorkflowRunResponse\`.

---
## sdk-reference/browser-automation/click
Source: https://skyvern.com/docs/sdk-reference/browser-automation/click.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# click

Click an element using a CSS selector, an AI prompt, or both. When both are given, the selector is tried first; if it fails, AI takes over.

 \`\`\`python Python theme={null}
 # Standard Playwright click
 await page.click("#submit-button")

 # AI-powered click (no selector needed)
 await page.click(prompt="Click the 'Submit' button")

 # Selector with AI fallback
 await page.click("#submit-button", prompt="Click the 'Submit' button")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Standard Playwright click
 await page.click("#submit-button");

 // AI-powered click (no selector needed)
 await page.click({ prompt: "Click the 'Submit' button" });

 // Selector with AI fallback
 await page.click("#submit-button", { prompt: "Click the 'Submit' button" });
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` / \`string\` \| No \| CSS selector for the target element. \|
\| \`prompt\` \| \`str\` / \`string\` \| No \| Natural language description of the element to click. \|
\| \`ai\` \| \`str\` / \`string\` \| No \| Controls AI behavior. \`"fallback"\` (default) tries the selector first, then AI. \`None\` / \`null\` disables AI. \|
\| \`\*\*kwargs\` \| \| No \| Standard Playwright click options (e.g., \`timeout\`, \`force\`, \`position\`). \|

Returns \`str \| None\` / \`string \| null\` -- the resolved selector used, or \`None\` if AI handled the click without a selector.

---
## sdk-reference/browser-automation/hover
Source: https://skyvern.com/docs/sdk-reference/browser-automation/hover.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# hover

Move the mouse over an element. Python only.

\`\`\`python theme={null}
\# Hover over a menu item
await page.hover("#menu-item")

\# Hover with a hold duration
await page.hover("#tooltip-trigger", hold\_seconds=1.5)

\# Hover with intention logging
await page.hover("#menu-item", intention="Hover over the main menu")
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` \| Yes \| CSS or XPath selector for the target element. \|
\| \`timeout\` \| \`float\` \| No \| Maximum time in milliseconds to wait for the element. Defaults to \`BROWSER\_ACTION\_TIMEOUT\_MS\`. \|
\| \`hold\_seconds\` \| \`float\` \| No \| How long to hold the hover, in seconds. Default \`0.0\`. \|
\| \`intention\` \| \`str\` \| No \| Description of the hover intent, used for logging. \|

Returns \`str\` - the resolved selector used.

---
## sdk-reference/browser-automation/type
Source: https://skyvern.com/docs/sdk-reference/browser-automation/type.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# type

Type text character-by-character into an input field. Unlike \`fill\`, this triggers keystroke events for each character - use it for fields that react to individual key presses (search autocomplete, OTP inputs). Python only.

\`\`\`python theme={null}
\# Character-by-character input
await page.type("#search", value="query text")

\# AI-powered type
await page.type(prompt="Type 'hello' into the search box")

\# Selector with AI fallback
await page.type("#search", value="query text", prompt="Type into the search field")

\# TOTP input
await page.type("#otp", totp\_identifier="my-app", totp\_url="otpauth://totp/...")
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` \| No \| CSS or XPath selector for the input field. \|
\| \`value\` \| \`str\` \| No \| Text to type character-by-character. \|
\| \`ai\` \| \`str\` \| No \| Controls AI behavior. Default \`"fallback"\` tries the selector first, then AI. \|
\| \`prompt\` \| \`str\` \| No \| Natural-language description of the target field. \|
\| \`totp\_identifier\` \| \`str\` \| No \| Identifier for a stored TOTP secret. \|
\| \`totp\_url\` \| \`str\` \| No \| \`otpauth://\` URI to generate a one-time password on the fly. \|

Returns \`str\` - the resolved selector used.

---
## sdk-reference/browser-automation/fill
Source: https://skyvern.com/docs/sdk-reference/browser-automation/fill.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# fill

Fill an input field using a CSS selector, an AI prompt, or both. Supports TOTP code injection for 2FA fields.

 \`\`\`python Python theme={null}
 # Standard Playwright fill
 await page.fill("#email", value="user@example.com")

 # AI-powered fill
 await page.fill(prompt="Fill 'user@example.com' in the email field")

 # Selector with AI fallback
 await page.fill("#email", value="user@example.com",
 prompt="Fill the email address field")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Standard Playwright fill
 await page.fill("#email", "user@example.com");

 // AI-powered fill
 await page.fill({ prompt: "Fill 'user@example.com' in the email field" });

 // Selector with AI fallback
 await page.fill("#email", "user@example.com", {
 prompt: "Fill the email address field",
 });
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` / \`string\` \| No \| CSS selector for the input field. \|
\| \`value\` \| \`str\` / \`string\` \| No \| The text value to fill into the field. \|
\| \`prompt\` \| \`str\` / \`string\` \| No \| Natural language description of the field and the value to enter. \|
\| \`ai\` \| \`str\` / \`string\` \| No \| Controls AI behavior. \`"fallback"\` (default) tries the selector first, then AI. \`None\` / \`null\` disables AI. \|
\| \`totp\_identifier\` / \`totpIdentifier\` \| \`str\` / \`string\` \| No \| Identifier for a stored TOTP secret to generate a one-time code. \|
\| \`totp\_url\` / \`totpUrl\` \| \`str\` / \`string\` \| No \| TOTP provisioning URL (\`otpauth://...\`) to generate a one-time code on the fly. \|
\| \`\*\*kwargs\` \| \| No \| Standard Playwright fill options (e.g., \`timeout\`, \`force\`). \|

Returns \`str\` / \`string\` -- the resolved selector used.

---
## sdk-reference/browser-automation/fill-form
Source: https://skyvern.com/docs/sdk-reference/browser-automation/fill-form.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# fill\_form

Fill a single-page form using AI. Pass a \`data\` dict describing the values to fill.

\`\`\`python theme={null}
await page.fill\_form(
 data={"name": "John Doe", "email": "john@example.com", "role": "Engineer"},
)

\# With a custom prompt to guide the AI
await page.fill\_form(
 data={"name": "John Doe", "email": "john@example.com"},
 prompt="Fill out the registration form with the provided user details",
)
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`data\` \| \`dict\[str, Any\]\` \| Yes \| Key-value pairs of form data to fill. \|
\| \`prompt\` \| \`str\` \| No \| Instruction for the AI. Defaults to \`"Fill out the form"\`. \|

\## Returns \`None\`

---
## sdk-reference/browser-automation/fill-autocomplete
Source: https://skyvern.com/docs/sdk-reference/browser-automation/fill-autocomplete.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# fill\_autocomplete

Fill an input with autocomplete/typeahead handling.

\`\`\`python theme={null}
await page.fill\_autocomplete(
 selector="#city",
 value="San Francisco",
 option\_selector=".autocomplete-option",
)
\`\`\`

\## Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` \| No \| CSS selector for the input field. \|
\| \`value\` \| \`str\` \| No \| The text value to type into the field. \|
\| \`prompt\` \| \`str\` \| No \| Natural language description of the field and value. \|
\| \`ai\` \| \`str\` \| No \| Controls AI behavior. \`"fallback"\` (default) tries the selector first, then AI. \|
\| \`option\_selector\` \| \`str\` \| No \| CSS selector for the autocomplete dropdown options. \|
\| \`wait\_seconds\` \| \`float\` \| No \| Seconds to wait for the dropdown to appear. Default \`1.5\`. \|
\| \`\*\*kwargs\` \| \| No \| Standard Playwright fill options (e.g., \`timeout\`, \`force\`). \|

\## Returns \`str\`

The resolved selector used.

---
## sdk-reference/browser-automation/fill-from-mapping
Source: https://skyvern.com/docs/sdk-reference/browser-automation/fill-from-mapping.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# fill\_from\_mapping

Fill form fields using an explicit index-based mapping produced by \`extract\_form\_fields\`.

\`\`\`python theme={null}
fields = await page.extract\_form\_fields()
await page.fill\_from\_mapping(
 form\_fields=fields,
 mapping={0: "John", 1: "Doe"}, # keys are field indices from extract\_form\_fields
 data={"name": "John Doe"},
)
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`form\_fields\` \| \`list\[dict\[str, Any\]\]\` \| Yes \| Field metadata returned by \`extract\_form\_fields\`. \|
\| \`mapping\` \| \`dict\[int, str \\\| list \\\| bool \\\| None\]\` \| Yes \| Map of field index to the value to fill. \|
\| \`data\` \| \`dict\[str, Any\] \\\| None\` \| No \| Optional source data for context. Defaults to \`None\`. \|

\## Returns \`None\`

---
## sdk-reference/browser-automation/fill-multipage-form
Source: https://skyvern.com/docs/sdk-reference/browser-automation/fill-multipage-form.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# fill\_multipage\_form

Fill a form that spans multiple pages, handling page transitions automatically.

\`\`\`python theme={null}
pages\_filled = await page.fill\_multipage\_form(
 data={"name": "John Doe", "email": "john@example.com", "address": "123 Main St"},
 max\_pages=5,
)
print(f"Filled {pages\_filled} pages")
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`data\` \| \`dict\[str, Any\]\` \| Yes \| Key-value pairs of form data to fill across all pages. \|
\| \`prompt\` \| \`str\` \| No \| Instruction for the AI. Defaults to \`"Fill out the form"\`. \|
\| \`next\_button\` \| \`str\` \| No \| Selector or description of the button to advance to the next page. \|
\| \`max\_pages\` \| \`int\` \| No \| Maximum number of pages to fill. Defaults to \`10\`. \|
\| \`timeout\_seconds\` \| \`float\` \| No \| Timeout in seconds for the entire operation. Defaults to \`300\`. \|

Returns \`int\` -- the number of pages filled.

---
## sdk-reference/browser-automation/extract
Source: https://skyvern.com/docs/sdk-reference/browser-automation/extract.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# extract

Extract structured data from the current page.

 \`\`\`python Python theme={null}
 data = await page.extract(
 "Extract all product names and prices",
 schema={
 "type": "array",
 "items": {
 "type": "object",
 "properties": {
 "name": {"type": "string"},
 "price": {"type": "number"},
 },
 },
 },
 )
 print(data)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const data = await page.extract({
 prompt: "Extract all product names and prices",
 schema: {
 type: "array",
 items: {
 type: "object",
 properties: {
 name: { type: "string" },
 price: { type: "number" },
 },
 },
 },
 });
 console.log(data);
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`prompt\` \| \`str\` / \`string\` \| Yes \| What to extract. \|
\| \`schema\` \| \`dict \\\| list \\\| str\` / \`Record\` \| No \| JSON schema for output. \|
\| \`error\_code\_mapping\` / \`errorCodeMapping\` \| \`dict\` / \`Record\` \| No \| Custom error codes. \|

Returns \`dict \| list \| str \| None\` / \`Record \| unknown\[\] \| string \| null\`.

---
## sdk-reference/browser-automation/extract-form-fields
Source: https://skyvern.com/docs/sdk-reference/browser-automation/extract-form-fields.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# extract\_form\_fields

Extract all form fields with metadata from the current page.

\`\`\`python theme={null}
fields = await page.extract\_form\_fields()
\# Returns list of dicts with field name, type, options, etc.
\`\`\`

\## Returns \`list\[dict\[str, Any\]\]\`

Each dict contains field name, type, options, and other metadata.

---
## sdk-reference/browser-automation/upload-file
Source: https://skyvern.com/docs/sdk-reference/browser-automation/upload-file.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# upload\_file

Upload one or more files to a file input. Pass a selector for direct Playwright behavior, a prompt for AI-powered file input detection, or both. Python only.

\`\`\`python theme={null}
\# Direct selector
await page.upload\_file("#file-input", files="/path/to/file.pdf")

\# Multiple files
await page.upload\_file("#file-input", files=\["/path/to/file1.pdf", "/path/to/file2.pdf"\])

\# AI-powered file input detection
await page.upload\_file(prompt="Upload the resume to the file input")

\# Selector with AI fallback
await page.upload\_file("#file-input", files="/path/to/file.pdf",
 prompt="Upload the resume to the file input")
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` \| No \| CSS or XPath selector for the file input. \|
\| \`files\` \| \`str \\\| list\[str\]\` \| No \| File path or list of file paths to upload. \|
\| \`prompt\` \| \`str\` \| No \| Natural-language description of the file input to target. \|
\| \`ai\` \| \`str\` \| No \| Controls AI behavior. Default \`"fallback"\` tries the selector first, then AI. \|

Returns \`str\` - the resolved selector used.

---
## sdk-reference/browser-automation/select-option
Source: https://skyvern.com/docs/sdk-reference/browser-automation/select-option.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# select\_option

Select an option from a dropdown using a CSS selector, an AI prompt, or both.

 \`\`\`python Python theme={null}
 # Standard Playwright select
 await page.select\_option("#country", value="us")

 # AI-powered select
 await page.select\_option(prompt="Select 'United States' from the country dropdown")

 # Selector with AI fallback
 await page.select\_option("#country", value="us",
 prompt="Select United States from country")
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 // Standard Playwright select
 await page.selectOption("#country", "us");

 // AI-powered select
 await page.selectOption({ prompt: "Select 'United States' from the country dropdown" });

 // Selector with AI fallback
 await page.selectOption("#country", "us", {
 prompt: "Select United States from country",
 });
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` / \`string\` \| No \| CSS selector for the \`\` element. \|
\| \`value\` \| \`str\` / \`string\` \| No \| The option value to select. \|
\| \`prompt\` \| \`str\` / \`string\` \| No \| Natural language description of the dropdown and the option to select. \|
\| \`ai\` \| \`str\` / \`string\` \| No \| Controls AI behavior. \`"fallback"\` (default) tries the selector first, then AI. \`None\` / \`null\` disables AI. \|
\| \`\*\*kwargs\` \| \| No \| Standard Playwright select options (e.g., \`timeout\`, \`force\`). \|

Returns \`list\[str\]\` / \`string\[\]\` -- the selected option values.

---
## sdk-reference/browser-automation/scroll
Source: https://skyvern.com/docs/sdk-reference/browser-automation/scroll.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# scroll

Scroll the page by a given number of pixels along the x and y axes.

\`\`\`python theme={null}
\# Scroll down 500px
await page.scroll(0, 500)
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`scroll\_x\` \| \`int\` \| Yes \| Horizontal scroll offset in pixels. Positive values scroll right. \|
\| \`scroll\_y\` \| \`int\` \| Yes \| Vertical scroll offset in pixels. Positive values scroll down. \|

Returns \`None\`.

---
## sdk-reference/browser-automation/validate
Source: https://skyvern.com/docs/sdk-reference/browser-automation/validate.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# validate

Validate the current page state with AI.

 \`\`\`python Python theme={null}
 is\_logged\_in = await page.validate("Check if the user is logged in")
 print(is\_logged\_in) # True or False
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const isLoggedIn = await page.validate("Check if the user is logged in");
 console.log(isLoggedIn); // true or false
 \`\`\`

\## Returns \`bool\` / \`boolean\`

\`True\` if the condition holds, \`False\` otherwise.

---
## sdk-reference/browser-automation/validate-mapping
Source: https://skyvern.com/docs/sdk-reference/browser-automation/validate-mapping.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# validate\_mapping

Validate that a field mapping is correct for the current form.

\`\`\`python theme={null}
fields = await page.extract\_form\_fields()
is\_valid = await page.validate\_mapping(
 form\_fields=fields,
 mapping={0: "John", 1: "Doe"},
 prompt="Validate the name fields are filled correctly",
)
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`form\_fields\` \| \`list\[dict\[str, Any\]\]\` \| Yes \| Field metadata returned by \`extract\_form\_fields\`. \|
\| \`mapping\` \| \`dict\[int, str \\\| list \\\| bool \\\| None\]\` \| Yes \| Map of field index to the value to validate. \|
\| \`prompt\` \| \`str \\\| None\` \| Yes \| Instruction describing what to validate. \|

Returns \`bool\` -- \`True\` if the mapping is valid, \`False\` otherwise.

---
## sdk-reference/browser-automation/locator
Source: https://skyvern.com/docs/sdk-reference/browser-automation/locator.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# locator

Locate an element using a CSS/XPath selector, an AI prompt, or both. When called with a \`prompt\` parameter, returns an \`AILocator\` - a lazy Playwright \`Locator\` that resolves the element's position via AI on first use.

\`\`\`python theme={null}
\# AI-powered: pass a natural-language prompt
locator = page.locator(prompt="the submit button")
await locator.click()

\# Full Playwright chaining works
text = await page.locator(prompt="the error message").text\_content()
\`\`\`

 When called with only a \`selector\` (no \`prompt\`), \`page.locator(selector)\` behaves exactly like the standard Playwright \`page.locator(selector)\` - no AI is involved.

\`\`\`python theme={null}
\# Standard Playwright selector - no AI, identical to vanilla Playwright
locator = page.locator("#submit-btn")
await locator.click()

\# Combine both: use the selector first, fall back to AI if it fails
locator = page.locator("#submit-btn", prompt="the submit button")
await locator.click()
\`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` \| No \| CSS or XPath selector passed to Playwright's built-in \`locator()\`. \|
\| \`prompt\` \| \`str\` \| No \| Natural-language description of the element. When provided, returns an \`AILocator\` that resolves via AI. \|
\| \`ai\` \| \`str\` \| No \| Controls AI behavior. Default \`"fallback"\` tries the selector first, then AI. \|
\| \`\*\*kwargs\` \| \| No \| Additional keyword arguments forwarded to Playwright's \`locator()\`. \|

Returns \`Locator\` - standard Playwright \`Locator\` when only a selector is given, or \`AILocator\` when a prompt is provided.

\### AILocator

When \`prompt\` is provided, the returned \`AILocator\` supports all standard Playwright \`Locator\` methods:

\\* \*\*Actions:\*\* \`click()\`, \`fill()\`, \`type()\`, \`select\_option()\`, \`check()\`, \`uncheck()\`, \`clear()\`, \`hover()\`, \`focus()\`, \`press()\`
\\* \*\*Queries:\*\* \`text\_content()\`, \`inner\_text()\`, \`inner\_html()\`, \`get\_attribute()\`, \`input\_value()\`, \`count()\`
\\* \*\*State:\*\* \`is\_visible()\`, \`is\_hidden()\`, \`is\_enabled()\`, \`is\_disabled()\`, \`is\_editable()\`, \`is\_checked()\`
\\* \*\*Chaining:\*\* \`first()\`, \`last()\`, \`nth()\`, \`filter()\`, \`locator()\`, \`get\_by\_text()\`, \`get\_by\_role()\`, \`get\_by\_label()\`, \`get\_by\_placeholder()\`
\\* \*\*Utilities:\*\* \`wait\_for()\`, \`screenshot()\`, \`playwright\_locator\` (access raw \`Locator\`)

---
## sdk-reference/browser-automation/prompt
Source: https://skyvern.com/docs/sdk-reference/browser-automation/prompt.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# prompt

Send a prompt to the LLM and get a structured response about the current page.

 \`\`\`python Python theme={null}
 result = await page.prompt(
 "What is the main heading on this page?",
 schema={"heading": {"type": "string"}},
 )
 print(result)
 \`\`\`

 \`\`\`typescript TypeScript theme={null}
 const result = await page.prompt(
 "What is the main heading on this page?",
 { heading: { type: "string" } },
 );
 console.log(result);
 \`\`\`

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`prompt\` \| \`str\` / \`string\` \| Yes \| The question or instruction to send to the LLM about the current page. \|
\| \`schema\` \| \`dict\` / \`Record\` \| No \| JSON schema that constrains the response shape. When provided, the LLM returns data matching this schema. \|
\| \`model\` \| \`dict\` / \`Record\` \| No \| LLM model configuration override. Use to select a different model for this call. \|

Returns \`dict \| list \| str \| None\` / \`Record \| unknown\[\] \| string \| null\`.

---
## sdk-reference/browser-automation/frame-list
Source: https://skyvern.com/docs/sdk-reference/browser-automation/frame-list.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# frame\_list

List all frames on the current page with metadata.

\`\`\`python theme={null}
frames = await page.frame\_list()
\`\`\`

\## Returns \`list\[dict\[str, Any\]\]\`

Metadata for each frame on the page.

---
## sdk-reference/browser-automation/frame-main
Source: https://skyvern.com/docs/sdk-reference/browser-automation/frame-main.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# frame\_main

Switch back to the main page frame.

\`\`\`python theme={null}
page.frame\_main()
\`\`\`

\## Returns \`dict\[str, str\]\`

---
## sdk-reference/browser-automation/frame-switch
Source: https://skyvern.com/docs/sdk-reference/browser-automation/frame-switch.md

\> ## Documentation Index
\> Fetch the complete documentation index at: https://skyvern.com/docs/llms.txt
\> Use this file to discover all available pages before exploring further.

\# frame\_switch

Switch the working context to an iframe. Exactly one parameter is required.

\`\`\`python theme={null}
\# By CSS selector
await page.frame\_switch(selector="#payment-iframe")

\# By frame name
await page.frame\_switch(name="checkout")

\# By index
await page.frame\_switch(index=0)
\`\`\`

\## Parameters

\| Parameter \| Type \| Required \| Description \|
\| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\- \| \-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`selector\` \| \`str\` \| No \| CSS selector for the iframe element. \|
\| \`name\` \| \`str\` \| No \| The \`name\` attribute of the iframe. \|
\| \`index\` \| \`int\` \| No \| Zero-based index of the iframe on the page. \|

 Exactly one of \`selector\`, \`name\`, or \`index\` must be provided.

\## Returns \`dict\[str, Any\]\`

Frame metadata for the switched-to iframe.

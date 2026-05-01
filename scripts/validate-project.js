const fs = require('fs');
const path = require('path');

const root = process.cwd();
const workflowPath = path.join(root, 'workflow', 'tiktok-viral-ai-automation.json');

const requiredFiles = [
  'README.md',
  'LICENSE',
  'requirements.txt',
  '.env.example',
  'src/tiktok_deep_scrape.py',
  'workflow/tiktok-viral-ai-automation.json',
  'workflow/README.md',
  'docs/SETUP.md',
  'docs/API.md',
  'docs/WORKFLOW.md',
  'docs/TROUBLESHOOTING.md',
];

const requiredNodes = [
  'Manual Test Trigger',
  'Scrape TikTok Trends',
  'Build Trend Prompt',
  'Generate Viral Script',
  'Ollama Chat Model',
];

const forbiddenPatterns = [
  { name: 'private 10.x API URL', pattern: /http:\/\/10\.\d+\.\d+\.\d+:\d+/ },
  { name: 'exported n8n credential block', pattern: /"credentials"\s*:/ },
  { name: 'exported n8n instance id', pattern: /"instanceId"\s*:/ },
  { name: 'stale n8n execute workflow mojibake', pattern: /Execute workflow|â/ },
  { name: 'old workflow file name', pattern: /TikTok_scrapping_bot\.json/ },
];

function fail(message) {
  console.error(`Validation failed: ${message}`);
  process.exitCode = 1;
}

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(root, file))) {
    fail(`missing required file: ${file}`);
  }
}

let workflow;
let workflowRaw = '';

try {
  workflowRaw = fs.readFileSync(workflowPath, 'utf8');
  workflow = JSON.parse(workflowRaw);
} catch (error) {
  fail(`workflow JSON is invalid: ${error.message}`);
}

if (workflow) {
  if (!Array.isArray(workflow.nodes)) {
    fail('workflow.nodes must be an array');
  }

  if (!workflow.connections || typeof workflow.connections !== 'object') {
    fail('workflow.connections must be an object');
  }

  const nodeNames = new Set(workflow.nodes.map((node) => node.name));

  for (const nodeName of requiredNodes) {
    if (!nodeNames.has(nodeName)) {
      fail(`missing required node: ${nodeName}`);
    }
  }

  const referencedNodes = [];

  function collectConnectionRefs(value) {
    if (Array.isArray(value)) {
      value.forEach(collectConnectionRefs);
      return;
    }

    if (!value || typeof value !== 'object') return;

    if (typeof value.node === 'string') {
      referencedNodes.push(value.node);
    }

    Object.values(value).forEach(collectConnectionRefs);
  }

  collectConnectionRefs(workflow.connections);

  for (const nodeName of referencedNodes) {
    if (!nodeNames.has(nodeName)) {
      fail(`connection references missing node: ${nodeName}`);
    }
  }

  for (const node of workflow.nodes) {
    if (Object.prototype.hasOwnProperty.call(node, 'credentials')) {
      fail(`node should not export credentials: ${node.name}`);
    }
  }
}

const textFiles = [
  'README.md',
  'CONTRIBUTING.md',
  'SECURITY.md',
  'CHANGELOG.md',
  'docs/SETUP.md',
  'docs/API.md',
  'docs/WORKFLOW.md',
  'docs/TROUBLESHOOTING.md',
  'workflow/README.md',
  'src/tiktok_deep_scrape.py',
  'workflow/tiktok-viral-ai-automation.json',
];

for (const file of textFiles) {
  const content = fs.readFileSync(path.join(root, file), 'utf8');

  for (const { name, pattern } of forbiddenPatterns) {
    if (pattern.test(content)) {
      fail(`${file} contains ${name}`);
    }
  }
}

if (!process.exitCode) {
  console.log('Project validation passed.');
}

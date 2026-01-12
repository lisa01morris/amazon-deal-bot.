import fs from "fs";
import path from "path";
import fetch from "node-fetch";

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

function readIfExists(file) {
  return fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "MISSING";
}

const context = {
  tree: fs.readdirSync(".", { withFileTypes: true })
    .map(f => (f.isDirectory() ? `[DIR] ${f.name}` : f.name))
    .join("\n"),

  nextSteps: readIfExists("NEXT_STEPS.md"),
  readme: readIfExists("README.md")
};

const prompt = `
You are an AI project manager.

Analyze this repository and respond with:
1. CURRENT STATE
2. WHAT IS BLOCKING PROGRESS
3. NEXT 3 ACTIONS (ordered, concrete)
4. OPTIONAL IMPROVEMENTS

Repository snapshot:
${JSON.stringify(context, null, 2)}
`;

async function run() {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OPENAI_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4.1-mini",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.2
    })
  });

  const data = await res.json();
  console.log("\n🧠 AI REVIEW RESULT:\n");
  console.log(data.choices[0].message.content);
}

run();

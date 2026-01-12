const fs = require('fs');

const requiredFiles = [
  'README.md',
  '.env.example',
  '.github/workflows',
  'NEXT_STEPS.md'
];

console.log('🔍 Project Health Check\n');

requiredFiles.forEach(file => {
  if (!fs.existsSync(file)) {
    console.log(`❌ Missing: ${file}`);
  } else {
    console.log(`✅ Found: ${file}`);
  }
});

console.log('\n🧭 NEXT ACTION:');
console.log('→ Open NEXT_STEPS.md and complete the first unchecked item.');

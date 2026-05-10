/**
 * ELOHIM SHARDS — Multi-faction AI combat game
 * Copyright (c) 2025 Kiliaan Vanvoorden / Bakery Street Project
 * License: MIT
 * Watermark: PRIMAX-AI-ELOHIM-BSP-2025
 * Repository: https://github.com/BoozeLee/elohim-forge
 * 
 * This software is provided as-is under the MIT license.
 * See LICENSE file or https://opensource.org/licenses/MIT
 */

// PRIMAX-AI-ELOHIM-BSP-2025

let PALETTES = {};
let QUESTS = {};
let NPC_VOICES = {};

// Load data files
async function loadGameData() {
  try {
    const [palRes, questRes, npcRes] = await Promise.all([
      fetch('data/palettes.json'),
      fetch('data/quest_graph.json'),
      fetch('data/npc_voices.json')
    ]);
    
    PALETTES = await palRes.json();
    QUESTS = await questRes.json();
    NPC_VOICES = await npcRes.json();
    console.log('✓ Game data loaded');
  } catch (e) {
    console.warn('⚠ Could not load data files (running locally?):', e.message);
  }
}

const SHARDS = [
  { name: 'Memory', rarity: 'Legendary', domain: 'Pointer arithmetic, allocation' },
  { name: 'Recursion', rarity: 'Legendary', domain: 'Infinite depth, base cases' },
  { name: 'Concurrency', rarity: 'Legendary', domain: 'Race conditions, deadlocks' },
  { name: 'Immutability', rarity: 'Epic', domain: 'Pure functions, referential transparency' },
  { name: 'Abstraction', rarity: 'Epic', domain: 'Interfaces, polymorphism' },
  { name: 'Compilation', rarity: 'Epic', domain: 'Parsing, ASTs, type inference' },
  { name: 'Entropy', rarity: 'Rare', domain: 'Randomness, chaos' },
  { name: 'State', rarity: 'Rare', domain: 'Mutability, side effects' },
  { name: 'Pattern', rarity: 'Rare', domain: 'Regex, structural recognition' },
  { name: 'Binding', rarity: 'Uncommon', domain: 'Closures, scoping' },
  { name: 'Flow', rarity: 'Uncommon', domain: 'Control structures, loops' },
  { name: 'Protocol', rarity: 'Uncommon', domain: 'Interfaces, contracts' },
  { name: 'Origin', rarity: 'Mythic', domain: 'Source code of reality' },
];

const GLITCH_LINES = [
  'system.load( shard_registry )...',
  'faction_alignments initializing...',
  'dragon_dream_engine: online',
  'scanning for Fractured Ones...',
  'compiling reality... OK',
  'shard_network: 13 nodes active',
  'awaiting player signature...',
  'code_elohim heartbeat: detected',
];

function renderShards() {
  const container = document.getElementById('shard-container');
  container.innerHTML = SHARDS.map(s =>
    `<div class="shard-item">
      <span>${s.name}</span>
      <span class="shard-rarity">${s.rarity}</span>
    </div>`
  ).join('');
}

function renderQuests() {
  const container = document.getElementById('quest-container');
  if (!container || !QUESTS.quests) return;
  
  container.innerHTML = Object.values(QUESTS.quests).slice(0, 4).map(q =>
    `<div class="quest-card ${q.type}">
      <div class="quest-title">${q.title}</div>
      <div class="quest-npc">📍 ${q.npc}</div>
      <div style="font-size: 0.75rem; color: var(--dim);">${q.description}</div>
    </div>`
  ).join('');
}

function displayNPCDialogue(npcKey) {
  const chatBox = document.getElementById('npc-chat');
  if (!chatBox || !NPC_VOICES.npcs[npcKey]) return;
  
  const npc = NPC_VOICES.npcs[npcKey];
  const lines = npc.dialogue_lines.greeting;
  const randLine = lines[Math.floor(Math.random() * lines.length)];
  
  const bubble = document.createElement('div');
  bubble.className = 'npc-dialogue-bubble';
  bubble.innerHTML = `<strong>${npc.name}:</strong> ${randLine}`;
  bubble.style.borderLeftColor = npc.color;
  
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function animateBackground(canvas) {
  const ctx = canvas.getContext('2d');
  let time = 0;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  function draw() {
    time += 0.005;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const cols = Math.ceil(canvas.width / 30);
    const rows = Math.ceil(canvas.height / 30);

    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const v = Math.sin(x * 0.3 + y * 0.2 + time * 2) * 0.5 + 0.5;
        const alpha = v * 0.15;
        ctx.fillStyle = `rgba(68, 255, 136, ${alpha})`;
        ctx.fillRect(x * 30, y * 30, 1, 1);
      }
    }

    ctx.strokeStyle = `rgba(255, 68, 136, ${0.05 + Math.sin(time) * 0.03})`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i < 5; i++) {
      const yPos = (Math.sin(time + i * 1.5) * 0.3 + 0.5) * canvas.height;
      ctx.moveTo(0, yPos);
      ctx.lineTo(canvas.width, yPos + Math.sin(time * 2 + i) * 20);
    }
    ctx.stroke();

    requestAnimationFrame(draw);
  }
  draw();
}

function cycleGlitch() {
  const el = document.getElementById('glitch-text');
  let i = 0;
  setInterval(() => {
    el.textContent = '> ' + GLITCH_LINES[i % GLITCH_LINES.length];
    el.style.color = '#44ff88';
    setTimeout(() => { el.style.color = ''; }, 200);
    i++;
  }, 3000);
}

function animateProgress() {
  const fill = document.getElementById('progress-fill');
  let width = 0;
  setInterval(() => {
    width = Math.sin(Date.now() / 5000) * 30 + 50;
    fill.style.width = width + '%';
  }, 100);
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadGameData();
  renderShards();
  renderQuests();
  animateBackground(document.getElementById('bg'));
  cycleGlitch();
  animateProgress();
  
  // Add NPC interaction
  setTimeout(() => displayNPCDialogue('scripting_sage'), 1500);
  setTimeout(() => displayNPCDialogue('memory_priest'), 4000);
});

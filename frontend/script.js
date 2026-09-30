// ==========================================
// PRINTFORGE AI — FRONTEND SCRIPT
// ==========================================
 
let generatedImages = [];
 
// ==========================================
// ELEMENTS
// ==========================================
 
const composer = document.getElementById("composer");
const ideaInput = document.getElementById("idea");
const charCount = document.getElementById("charCount");
 
const generateBtn = document.getElementById("generateBtn");
const buttonText = document.getElementById("buttonText");
 
const generationStatus = document.getElementById("generationStatus");
const statusText = document.getElementById("statusText");
 
const gallerySection = document.getElementById("gallery");
const previewGallery = document.getElementById("previewGallery");
const previewCount = document.getElementById("previewCount");
 
const pdfBar = document.getElementById("pdfBar");
const createPdfBtn = document.getElementById("createPdfBtn");
const downloadPdfBtn = document.getElementById("downloadPdfBtn");
 
const settingsTrigger = document.getElementById("settingsTrigger");
const settingsPopover = document.getElementById("settingsPopover");
const popoverScrim = document.getElementById("popoverScrim");
 
const navToggle = document.getElementById("navToggle");
const navbar = document.querySelector(".navbar");
 
const authModal = document.getElementById("authModal");
const authClose = document.getElementById("authClose");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const loginSubmit = document.getElementById("loginSubmit");
const signupSubmit = document.getElementById("signupSubmit");
const loginNote = document.getElementById("loginNote");
const signupNote = document.getElementById("signupNote");
 
// ==========================================
// CHARACTER COUNTER
// ==========================================
 
if (ideaInput && charCount) {
  ideaInput.addEventListener("input", () => {
    charCount.textContent = ideaInput.value.length;
  });
}
 
// ==========================================
// COMPOSER FOCUS STATE (RGB glow)
// ==========================================
 
if (ideaInput && composer) {
  ideaInput.addEventListener("focus", () => composer.classList.add("is-focused"));
  ideaInput.addEventListener("blur", () => composer.classList.remove("is-focused"));
 
  ideaInput.addEventListener("keydown", event => {
    if (event.ctrlKey && event.key === "Enter") {
      generateBook();
    }
  });
}
 
// ==========================================
// SETTINGS POPOVER
// ==========================================
 
function openSettings() {
  settingsPopover.classList.add("open");
  popoverScrim.classList.add("show");
  settingsTrigger.setAttribute("aria-expanded", "true");
}
 
function closeSettings() {
  settingsPopover.classList.remove("open");
  popoverScrim.classList.remove("show");
  settingsTrigger.setAttribute("aria-expanded", "false");
}
 
if (settingsTrigger) {
  settingsTrigger.addEventListener("click", event => {
    event.stopPropagation();
    const isOpen = settingsPopover.classList.contains("open");
    isOpen ? closeSettings() : openSettings();
  });
}
 
if (popoverScrim) {
  popoverScrim.addEventListener("click", closeSettings);
}
 
document.addEventListener("click", event => {
  if (
    settingsPopover &&
    settingsPopover.classList.contains("open") &&
    !settingsPopover.contains(event.target) &&
    event.target !== settingsTrigger
  ) {
    closeSettings();
  }
});
 
document.addEventListener("keydown", event => {
  if (event.key === "Escape") {
    closeSettings();
    closeAuth();
  }
});
 
// ==========================================
// MOBILE NAV
// ==========================================
 
if (navToggle) {
  navToggle.addEventListener("click", () => {
    const isOpen = navbar.classList.toggle("nav-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}
 
document.querySelectorAll(".nav-mobile a").forEach(link => {
  link.addEventListener("click", () => navbar.classList.remove("nav-open"));
});
 
// ==========================================
// AUTH MODAL
// ==========================================
 
function openAuth(type) {
  authModal.classList.add("show");
  loginForm.classList.toggle("active", type === "login");
  signupForm.classList.toggle("active", type !== "login");
}
 
function closeAuth() {
  authModal.classList.remove("show");
}
 
document.querySelectorAll("[data-open-auth]").forEach(button => {
  button.addEventListener("click", () => openAuth(button.dataset.openAuth));
});
 
if (authClose) authClose.addEventListener("click", closeAuth);
 
if (authModal) {
  authModal.addEventListener("click", event => {
    if (event.target === authModal) closeAuth();
  });
}
 
// Frontend-only preview: no backend auth is connected yet.
if (loginSubmit) {
  loginSubmit.addEventListener("click", () => {
    loginNote.textContent = "Sign-in isn't connected yet — this is a UI preview.";
  });
}
 
if (signupSubmit) {
  signupSubmit.addEventListener("click", () => {
    signupNote.textContent = "Account creation isn't connected yet — this is a UI preview.";
  });
}
 
// ==========================================
// GENERATION STATUS MESSAGES
// ==========================================
 
const loadingMessages = [
  "Generating your coloring pages...",
  "Creating page concepts...",
  "Rendering illustrations...",
  "Finalizing your pages..."
];
 
let loadingInterval;
 
// ==========================================
// GENERATE BOOK
// ==========================================
 
async function generateBook() {
  const idea = ideaInput.value.trim();
 
  if (!idea) {
    ideaInput.focus();
    ideaInput.style.borderColor = "#ef4da0";
    setTimeout(() => { ideaInput.style.borderColor = ""; }, 1200);
    return;
  }
 
  generateBtn.disabled = true;
  buttonText.textContent = "Creating...";
  composer.classList.add("is-generating");
 
  generationStatus.classList.add("show");
  let messageIndex = 0;
  statusText.textContent = loadingMessages[0];
 
  loadingInterval = setInterval(() => {
    messageIndex = (messageIndex + 1) % loadingMessages.length;
    statusText.textContent = loadingMessages[messageIndex];
  }, 2200);
 
  try {
    const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        idea,
        printSize: document.getElementById("printSize").value,
        aspectRatio: document.getElementById("aspectRatio").value,
        resolution: document.getElementById("resolution").value,
        fileFormat: document.getElementById("fileFormat").value,
        illustrationStyle: document.getElementById("illustrationStyle").value,
        imageQuality: document.getElementById("imageQuality").value
    })
});
 
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
 
    const data = await response.json();
 
    if (!data.success) {
      throw new Error(data.error || "Book generation failed.");
    }
 
    generatedImages = data.images || [];
    showGallery(generatedImages);
 
  } catch (error) {
    console.error("Generation error:", error);
    statusText.textContent = "Something went wrong. Please try again.";
    setTimeout(() => {
      generationStatus.classList.remove("show");
    }, 2500);
 
  } finally {
    clearInterval(loadingInterval);
    generateBtn.disabled = false;
    buttonText.textContent = "Create";
    composer.classList.remove("is-generating");
    if (generatedImages.length) {
      generationStatus.classList.remove("show");
    }
  }
}
 
if (generateBtn) generateBtn.addEventListener("click", generateBook);
 
// ==========================================
// GALLERY
// ==========================================
 
function showGallery(images) {
  previewGallery.innerHTML = "";
 
  if (!images || images.length === 0) {
    previewGallery.innerHTML = `<div class="empty-preview">No images generated yet.</div>`;
  } else {
    images.forEach((image, index) => {
      const card = document.createElement("div");
      card.className = "gallery-card";
      card.innerHTML = `
        <div class="gallery-image-wrap">
          <img src="${image}" alt="Coloring page ${index + 1}" loading="lazy">
        </div>
        <div class="gallery-card-footer">
          <span>Page ${String(index + 1).padStart(2, "0")}</span>
          <a class="card-download" href="${image}" download="coloring-page-${index + 1}.png">Download</a>
        </div>
      `;
      previewGallery.appendChild(card);
    });
  }
 
  previewCount.textContent = images ? images.length : 0;
  gallerySection.classList.add("show");
 
  createPdfBtn.disabled = false;
  createPdfBtn.textContent = "Create PDF";
  downloadPdfBtn.style.display = "none";
 
  setTimeout(() => {
    gallerySection.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 250);
}
 
// ==========================================
// CREATE PDF
// ==========================================
 
async function createPDF() {
  if (!generatedImages || generatedImages.length === 0) {
    return;
  }
 
  createPdfBtn.disabled = true;
  createPdfBtn.textContent = "Creating PDF...";
 
  try {
    const response = await fetch("/create-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ images: generatedImages })
    });
 
    if (!response.ok) {
      throw new Error(`PDF server error: ${response.status}`);
    }
 
    const data = await response.json();
 
    if (!data.success) {
      throw new Error(data.error || "PDF creation failed.");
    }
 
    createPdfBtn.textContent = "PDF Ready";
    downloadPdfBtn.href = data.pdf_url;
    downloadPdfBtn.style.display = "inline-flex";
 
  } catch (error) {
    console.error("PDF error:", error);
    createPdfBtn.disabled = false;
    createPdfBtn.textContent = "Create PDF";
  }
}
 
if (createPdfBtn) createPdfBtn.addEventListener("click", createPDF);
 
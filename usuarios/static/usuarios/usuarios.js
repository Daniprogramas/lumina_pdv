/* Mantemos APENAS os atalhos de teclado úteis para o PDV.
   Toda a parte de Acessibilidade (Dark mode, Fontes, Leitor) 
   agora é controlada pelo base_usuarios.html de forma global! */

document.addEventListener("keydown", function(event) {
  // Se apertar ESC, volta para o menu principal
  if(event.key === "Escape") {
    window.location.href = "/";
  }
  
  // Se apertar Enter (e não estiver num campo de texto de múltiplas linhas), tenta submeter o formulário
  if(event.key === "Enter") {
    // Evita que o Enter submeta acidentalmente se a pessoa estiver apenas a interagir com um botão normal
    if (document.activeElement.tagName !== "BUTTON") {
        let btn = document.querySelector("button[type=submit]");
        if(btn) btn.click();
    }
  }
});
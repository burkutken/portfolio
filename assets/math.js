(() => {
  if (!window.katex) return;
  document.querySelectorAll('.math').forEach(element => {
    const formula = element.textContent;
    katex.render(formula, element, {
      displayMode: element.dataset.display === 'true',
      throwOnError: false,
      trust: false,
      strict: 'warn',
      output: 'htmlAndMathml'
    });
  });
})();

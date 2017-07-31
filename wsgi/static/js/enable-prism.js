//Vanilla method for adding new elements
function addElement(parent, tagName, attributes) {
    var newElement = document.createElement(tagName);
    for (var attrName in attributes) {
        newElement.setAttribute(attrName, attributes[attrName]);
    }
    parent.appendChild(newElement);
}
// Detect old browsers and bail out early
if (document.querySelectorAll && document.documentElement.classList) {
    // update code snippets so that they use the standards-friendly class name
    var codeSnippets = document.querySelectorAll('pre code');
    for (var i = 0; i < codeSnippets.length; i++) {
        var languageClass = codeSnippets[i].classList.item(0);
        languageClass = 'language-' + languageClass;
        codeSnippets[i].classList.add(languageClass);
    }

    //manually import prism.js and dependencies
    addElement(document.head, 'link', {'rel': 'stylesheet', 'href': '/static/css/prism.css'});
    addElement(document.body, 'script', {'src': '/static/js/prism.js'});

    document.documentElement.classList.add('prism');
}
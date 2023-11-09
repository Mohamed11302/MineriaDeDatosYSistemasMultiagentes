// Begin Pushing PDF Info to Google Analytics

document.addEventListener("click", function(e){
  e = e || event;
  var from = findParent('a',e.target || e.srcElement);
  if (from){
     if (e.target.href.toLowerCase().indexOf('.pdf') !== -1){
     //_gaq.push(['_trackEvent', 'PDFs', 'Downloaded', e.target.href.toLowerCase()]);
	 gtag('event', 'PDFs', { event_category: 'PDFs', event_action: 'Downloaded', event_label: e.target.href.toLowerCase()});
   }
  }
}
);


function findParent(tagname,el){
  if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
    return el;
  }
  while (el = el.parentNode){
    if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
      return el;
    }
  }
  return null;
}

// End Pushing PDF Info to Google Analytics
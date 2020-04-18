function upDate(previewPic){

 	//taking the previewPic's source url and appending into background image
    document.getElementById("image").style.backgroundImage='url(' +previewPic.src+ ')';

 	//taking the previewPic's alt and substituting into innerHTML
    document.getElementById("image").innerHTML=previewPic.alt;
	
}

function unDo(){

	//resetting to default
	document.getElementById("image").style.backgroundImage='url()';
	document.getElementById("image").innerHTML='Hover over an image below to display here.';
	
}

// when the check box is selected
function billingFunction(){
    if (same.checked){
      // TO save value from shipping information 
      var name=document.getElementById("shippingName").value;
      var zip=document.getElementById("shippingZip").value;
      billingName.setAttribute('value',name);
      billingZip.setAttribute('value',zip);
      // This will not let them edit the text
      document.getElementById("billingZip").disabled = true;
      document.getElementById("billingName").disabled = true;
    }
   // When checkbox isn't selected
		else{ 
		  billingZip.setAttribute('value',"");
      billingName.setAttribute('value',"");
      document.getElementById("billingName").disabled = false;
      document.getElementById("billingZip").disabled = false;
    }}  

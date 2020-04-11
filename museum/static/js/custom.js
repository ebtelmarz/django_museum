$(document).ready(function(){

  $(".dateinput").datepicker({changeYear: true,changeMonth: true});

    $(function() {
	$('#example1').timeliny({
		order: 'asc',
		className: 'timeliny',
		wrapper: '<div class="timeliny-wrapper"></div>',
		boundaries: 2,
		animationSpeed: 250,
        hideBlankYears: false,
		onInit: function() {},
		onDestroy: function() {},
		afterLoad: function(currYear) {},
		onLeave: function(currYear, nextYear) {},
		afterChange: function(currYear) {},
		afterResize: function() {}
	    });
    });

   var completes = document.querySelectorAll(".complete");
var toggleButton = document.getElementById("toggleButton");


function toggleComplete(){
  var lastComplete = completes[completes.length - 1];
  lastComplete.classList.toggle('complete');
}

toggleButton.onclick = toggleComplete;

});
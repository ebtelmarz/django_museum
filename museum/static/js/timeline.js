            function pallini(){
                var active = document.querySelectorAll("i.fas.fa-map-marker-alt.selected");
                var disactive = document.querySelectorAll("i.fas.fa-map-marker-alt")[0];
                //var pallino = document.querySelectorAll(".point");
                var next = document.getElementById("next");
                var prev = document.getElementById("prev");

                console.log(active);

                function show(){
                    //var currentli = disactive[0];
                    disactive.classList.add('selected');
                }
                next.onclick = show();

                function hide(){
                    var currentli = active[active.length -1];
                    currentli.classList.remove('selected');

                }
                prev.onclick = hide();
            }
















            /*var completes = document.querySelectorAll(".complete");
            var toggleButton = document.getElementById("toggleButton");
            var toggleButton_next = document.getElementById("toggleButton_next");

                function toggleComplete(){
                    var lastComplete = completes[completes.length - 1];
                    lastComplete.classList.toggle('complete');
                }

                function togglePrev(){
                    var lastComplete = completes[completes.length -1]
                    lastComplete.classList.toggle('')
                }

            toggleButton.onclick = togglePrev;
            toggleButton_next.onclick = toggleComplete;*/
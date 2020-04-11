            var completes = document.querySelectorAll(".complete");
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
            toggleButton_next.onclick = toggleComplete;

            var active = document.querySelectorAll(".selected");
            var pallino = document.querySelectorAll(".pallino");
            var next = document.getElementById("next")

                function show(){
                    var currentli = pallino[]
                }
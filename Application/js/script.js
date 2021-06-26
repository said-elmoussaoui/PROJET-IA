        let base64Image;
        $("#image-tester").change(function() {
            let reader = new FileReader();
            reader.onload = function(e) {
                let dataURL = reader.result;
                $('#image-choix').attr("src", dataURL);
                base64Image = dataURL.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
            }
            reader.readAsDataURL($("#image-tester")[0].files[0]);
            $("#res").text("");
            $("#prob").text("");

        });

        $("#preBtn").click(function(){
                let message = {
                image: base64Image
        }
            $.post("http://127.0.0.1:5000/predict", JSON.stringify(message), function(response){
                if(response.prediction.resultat ==  "Test Covid19 Positif"){
                    $("#res").css('color','red');
                    $("#prob").css('color','red');
                }else if(response.prediction.resultat == "Test Covid19 Négatif"){
                    $("#res").css('color','white');
                    $("#prob").css('color','white');
                }
                $("#res").text(response.prediction.resultat);
                $("#prob").text(response.prediction.precision.toFixed(2)*100+"%");
            });
        });

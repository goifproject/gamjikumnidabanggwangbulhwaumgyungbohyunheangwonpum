onload = function() {


    (document.querySelector("#snapshot-esc")).addEventListener("click", function () {
        (document.querySelector("#snapshot-cover")).classList.add("display-none");
    });

    (document.querySelector("#video-esc")).addEventListener("click", function () {
        (document.querySelector("#video-cover")).classList.add("display-none");
    });


    // 카메라 버튼
    var cameraButton = document.querySelector("#camera-button");

    // 카메라 버튼을 누름
    cameraButton.addEventListener("click", function () {
        (document.querySelector("#video-cover")).classList.remove("display-none");


        // 버튼 반응
        var elem = document.querySelector(".tap-target");
        var instance = M.TapTarget.getInstance(elem);
        instance.open();

        // 카메라 작동
        var videoTracks;
        var constraints = {
            audio: false,
            video: {
                width: { min: 1024, ideal: 1280, max: 1920 },
                height: { min: 776, ideal: 720, max: 1080 },
                facingMode: { exact: "environment" },
            }
        };
        var promise = navigator.mediaDevices.getUserMedia(constraints);
        promise.then(function(stream) {
            var player = document.querySelector('#player');

            player.srcObject = stream;
            videoTracks = stream.getVideoTracks();
            player.onloadedmetadata = function(e) {
                player.play();
            };
        }).catch(function(err) {
            console.log(err.name + ": " + err.message);
        });

        // 캡쳐하고 캔버스에 보여줌
        var snapshotCanvas = document.querySelector('#snapshot');
        var captureButton = document.querySelector('#capture');
        captureButton.addEventListener('click', function() {
            var context = snapshot.getContext('2d');
            // Draw the video frame to the canvas.
            context.drawImage(player, 0, 0, snapshotCanvas.width, snapshotCanvas.height);

            
            // document.querySelector('#inp_img').value = context.getImageData(0, 0, snapshotCanvas.width, snapshotCanvas.height);
            (document.querySelector("#snapshot-cover")).classList.remove("display-none");

            document.querySelector('#inp_img').value = snapshotCanvas.toDataURL("image/png");
        });
    })

    // 캔버스에서 서버로 이미지 전송
    // var imageTransfer = document.querySelector("#image-transfer");
    // imageTransfer.addEventListener("click", function() {
    //     var canvas = document.querySelector('#snapshot');
    //     var context = canvas.getContext('2d');
    //     document.querySelector('#inp_img').value = context.getImageData(0, 0, 320, 240);
    // });
    // function prepareImg() {
    //     var canvas = document.querySelector('#snapshot');
    //     document.querySelector('#inp_img').value = canvas.toDataURL();
    // }



    // 메뉴 버튼
    var menuButton = document.querySelector("#menu-button");

    // 메뉴 버튼 클릭
    menuButton.addEventListener("click", function () {
        var elem = document.querySelector(".sidenav")
        var instance = M.Sidenav.getInstance(elem);
        instance.open();
    });




    (document.querySelector("#bt_upload")).addEventListener("click", function () {
        M.toast({html: '3초 기다리세요'})
        serverResults(); 
    });
    function serverResults() {
        
        setTimeout(function () {
            M.toast({html: '나옵니다'})
            let path;
            let results;
            let asdf = [];
            let k = 0;

            // 이미지 값
            var qwer = (document.querySelector("#inp_img")).value;

            path = fetch('http://ngdb.kr:3212/ocr/base2info/',{
                method: "post",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: JSON.stringify({
                    "base64" : qwer
                })
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (myJSON) {
                // results = myJSON.amount;
                results = myJSON;
                if (results["code"]) {
                    for (let i = 0; i < selectedFilters.length; i++) {
                        for (let j = 0; i < results.simple.length; j++) {
                            if (selectedFilters[i] == results.simple[j]) {
                                asdf[k] = selectedFilters[i];
                                k++;
                            }
                        }
                    }
                    if (asdf) {
                        alert("귀하께서 설정하신 " + asdf + "가 식품에 들어있습니다.");
                    } else {
                        alert("안전하게 드실 수 있는 식품입니다.");
                    }
                } else {
                    M.toast({html: '사진을 다시 찍어주세요'})
                }
            });
        }, 3000);
            
    };


    // var asdf = [];
    // for (let i = 0; i < selectedFilters.length; i++) {
    //     if (results.simple.includes(selectedFilters[i])) {
    //         asdf = results.simple.includes(selectedFilters[i])
    //     }
    // }
    

    // 필터 선택
    // 필터 담는 변수
    var filters = document.querySelectorAll(".filter");

    // 선택된 필터들 담는 배열
    var count = 0;
    var selectedFilters = [];

    for (let filter of filters) {
        filter.addEventListener("click", function () {
            if (filter.classList.contains("selected")) {
                filter.classList.remove("selected");
                selectedFiltersRemove(filter.id);
                count--;
            } else {
                filter.classList.add("selected");
                selectedFilters[count] = filter.id;
                count++;
            }
        })
    }

    // 선택된 필터들 담는 배열 지우는 함
    function selectedFiltersRemove(id) {
        for (var i = 0; i < count; i++) {
            if (selectedFilters[i] == id) {
                for (i; i < count; i++) {
                    selectedFilters[i] = selectedFilters[i + 1];
                }
                break;
            }
        }
    }



    (document.querySelector("#test")).addEventListener("click", function () {
        alert(selectedFilters);
    })



};

// 버튼 누르면 안내 원이 튀어나옴
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tap-target');
    var instances = M.TapTarget.init(elems);
});

// 사이드 메뉴
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(
        elems, {
            // 사이드 메뉴가 모두 닫히면 실행되는 함수
            onCloseEnd : function () {
                // 메뉴의 포커스가 풀리게
                document.querySelector(".menu__wrapper > div").blur();
            },
        
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});
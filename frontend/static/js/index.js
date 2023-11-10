var blockImages = [];

for (var i = 1; i <= 7; i++) {
    var blockImg = new Image();
    blockImg.src = "../static/img/" + i + ".png";
    blockImages.push(blockImg);
}
function createFallingBlock() {
    const block = document.createElement('div');
    block.className = 'tetris-block';
    const randomLeft = Math.random() * 100 + '%';
    block.style.left = randomLeft;
    const randomImage = Math.floor(Math.random() * 7); 
    const blockImg = blockImages[randomImage].cloneNode(true);
    
    const randomRotate = Math.floor(Math.random() * 4); 
    blockImg.style.transform = 'rotate('+randomRotate*90+'deg)';

    block.appendChild(blockImg);
    document.body.appendChild(block);

    setTimeout(function () {
        block.remove();
    }, 5000);
}setInterval(function() {      createFallingBlock();    }, 1000);


function startPortScan() {
    let ipAddress = document.querySelector('#ip').value;
    let minPort = document.querySelector('.search-input.port').value;
    let maxPort = document.querySelector('.search-input.port2').value;
    let Stype = 's1';
    document.getElementsByName('scanner').forEach((node) => {
        if(node.checked)  {  Stype = node.value;  }
    }) 

    if(!ipAddress){
        alert('IP주소를 입력해주세요.');
        return;
    }

    var ips = ipAddress.split('.');
    if(ips.length!=4){
        alert('IP주소를 제대로 입력해주세요.');
        return;
    }
    
    if(!minPort) {document.querySelector('.search-input.port').value = 0; minPort=0;}
    if(!maxPort) {document.querySelector('.search-input.port2').value = 65535; maxPort=65535;}
    if(minPort>maxPort){
        alert('최소 포트가 더 크게 입력되었습니다.');
        return;
    }

    const scanButton = document.getElementById('scanButton');
    const scanResult = document.getElementById('scanResult');
    const loadingPage = document.getElementById('loadingPage');
    scanButton.disabled = true;
    loadingPage.style.display='inline';
    scanResult.innerHTML = '<h2>IP '+ipAddress+' 검색중..</h2>'

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ip: ipAddress,minPort:minPort,maxPort:maxPort,Stype:Stype }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); 
    })
    .then(data => {
        scanButton.disabled = false;
        loadingPage.style.display='none';
        if(data.error){
            alert('에러발생: '+data.error);
            document.getElementById("scanResult").innerHTML = "오류 발생: " + data.error;
            return;
        }
        const resultDiv = document.getElementById('scanResult');
        if (Object.keys(data).length>0) {
            resultDiv.innerHTML = '<h2>['+ipAddress+']<h2>';

            for (const port in data) {
                if (data.hasOwnProperty(port)) {
                    const status = data[port];
                    const div = document.createElement('div');

                    const heading = document.createElement('h3');
                    heading.textContent = `포트: ${port} =>[${status[2]}]`;
                    div.appendChild(heading);
                    if(status!='open'){
                        console.log(status[1])
                        const details = document.createElement('details');
                        const summary = document.createElement('summary');
                        summary.textContent = status[0];
                        const detailsContent = document.createElement('div');
                        detailsContent.style.padding = '30px';
                        detailsContent.textContent = status[1];
                    
                        details.appendChild(summary);
                        details.appendChild(detailsContent);
                        div.appendChild(details);
                        summary.id='summary'
                    }

                    resultDiv.appendChild(div);

                    if(status!='open')   div.addEventListener("mousedown", (e) => {
                        if(e.target.id!='summary')   details.open = !details.open;
                    });
                }
            }
        } else {
            resultDiv.innerHTML = '결과없음';
        }
    })
    .catch(error => {
        scanButton.disabled = false;
        loadingPage.style.display='none';
        document.getElementById("scanResult").innerHTML = "오류 발생: " + error;
    });
}
let started = false;

let startBtn, fileInput, fileLabel, data = [];

const RATIO = 0.5/6371000;

console.log('Loaded');
startBtn = document.querySelector('#start');
fileInput = document.querySelector('#fileInput');
fileInfo = document.querySelector('#fileInfo');

startBtn.disabled = true;
startBtn.classList = 'btn disabled'
startBtn.onclick = () => {
  if(!startBtn.disabled)started = true;
}

fileInput.onchange = e => {
  fileInfo.innerHTML = fileInput.files[0].name;
  parseFile(fileInput.files[0]);
}


const parseFile = file => {
  console.log('Parsing file', file)
  Papa.parse(file, {
    complete: function(results){
      for(let i=0;i<results.data.length-1;i++){
        data.push(results.data[i].map(r => parseFloat(r) * RATIO));
      }
    }
  });

  startBtn.disabled = false;
  startBtn.classList = 'btn';
  console.log(data);
}

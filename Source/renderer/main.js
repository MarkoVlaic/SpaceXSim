const { Scene, PerspectiveCamera, WebGLRenderer, Mesh, SphereGeometry, MeshPhongMaterial, AmbientLight, DirectionalLight } = THREE;

let scene, camera, renderer; //Rendering elements
let earth; //Earth model
let clouds;
let rocket;

let iterationIndex = -1;
let moveInterval;

window.onload = () => {
  //Initialize the scene, camera and renderer. After this we can render to screen
  const init = () => {
    scene = new Scene();

    const guih = document.querySelector('#gui').offsetHeight; //Height of the gui container
    camera = new PerspectiveCamera(45, window.innerWidth/(window.innerHeight-guih), 0.01, 1000); //Camera with 45 degree FOV, 0.1 near clipping plane and 1000 far clipping plane

    camera.position.z = 2; //Move the camera from the center

    renderer = new WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight - guih);
    document.querySelector('#renderContainer').appendChild(renderer.domElement);

    window.onresize = () => {
      camera.aspect = window.innerWidth/(window.innerHeight-guih);
      camera.updateProjectionMatrix();

      renderer.setSize(window.innerWidth, window.innerHeight-guih);
    }
  }

  //Create all objects in the scene
  const initGeometry = () => {
    //Setup the earth model
    let geometry = new SphereGeometry(0.5, 32, 32); //Geometry for the earth model
    let material = new MeshPhongMaterial();

    const loader = new THREE.TextureLoader();
    loader.crossOrigin = true;

    material.map = loader.load('static/earthmap1k.jpg'); //Load the earth texture (map of the earth)
    console.log('Earthmap1k.jpg', material.map);
    material.bumpMap = loader.load('static/earthbump1k.jpg'); //Load the bump map (terrain)
    material.bumpScale = 0.05; //Scale the bumps down so that everything looks normal

    material.specularMap = loader.load('static/earthspec1k.jpg'); //light reflection
    material.specular = new THREE.Color('grey');

    earth = new Mesh(geometry, material); //Create the earth model
    earth.recieveShadow = false;
    scene.add(earth);

    geometry = new SphereGeometry(0.505, 32, 32);
    let cloudTex = loader.load('static/clouds.jpg');

    material = new MeshPhongMaterial({
      map: cloudTex,
      side: THREE.DoubleSide,
      opacity: 0.28,
      transparent: true,
      depthWrite: false
    });1

    clouds = new Mesh(geometry, material);
    clouds.castShadow = false;
    clouds.renderOrder = 1;
    scene.add(clouds);
  }

  //Create lighting for the scene
  const initLight = () => {
    let light = new AmbientLight(0x555555, 1);
    scene.add(light);
    light = new DirectionalLight(0xffffff, 0.4);
    light.position.set(100, 100, 100);
    scene.add(light);
  }

  const render = () => {
    requestAnimationFrame(render);
    clouds.rotation.y += 0.0003;

    if(started){
      if(iterationIndex == -1)instantiateRocket();
    }

    renderer.render(scene, camera);
    //console.log(started);
  }

  const instantiateRocket = () => {
    let geometry = new SphereGeometry(0.01, 10, 10);
    let material = new MeshPhongMaterial({color: 0xD162D1});

    let rocket = new Mesh(geometry, material);
    rocket.position.x = data[0][0];
    rocket.position.y = data[0][1];
    rocket.position.z = data[0][2];

    scene.add(rocket);

    iterationIndex++;

    moveInterval = setInterval(moveRocket, 100);
  }

  const moveRocket = () => {
    iterationIndex++;
    if(iterationIndex < data.length){
      rocket.position.x = data[iterationIndex][0];
      rocket.position.y = data[iterationIndex][1];
      rocket.position.z = data[iterationIndex][2];
    }else {
      started = false;
      iterationIndex = -1;

      alert('done');
      clearInterval(moveInterval);
    }
  }

  init();
  initGeometry();
  initLight();
  requestAnimationFrame(render);
}

const { Scene, PerspectiveCamera, WebGLRenderer, Mesh, SphereGeometry, MeshPhongMaterial, AmbientLight, DirectionalLight } = THREE;

let scene, camera, renderer; //Rendering elements
let earth; //Earth modle

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
    const geometry = new SphereGeometry(0.5, 32, 32); //Geometry for the earth model
    const material = new MeshPhongMaterial();

    const loader = new THREE.TextureLoader();
    loader.crossOrigin = true;

    material.map = loader.load('static/earthmap1k.jpg'); //Load the earth texture (map of the earth)

    material.bumpMap = loader.load('static/earthbump1k.jpg'); //Load the bump map (terrain)
    material.bumpScale = 0.05; //Scale the bumps down so that everything looks normal

    material.specularMap = loader.load('static/earthspec1k.jpg'); //light reflection
    material.specular = new THREE.Color('grey');

    earth = new Mesh(geometry, material); //Create the earth model
    scene.add(earth);
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

    renderer.render(scene, camera);
  }

  init();
  initGeometry();
  initLight();
  requestAnimationFrame(render);
}

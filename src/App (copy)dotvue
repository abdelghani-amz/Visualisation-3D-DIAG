<template>
  <v-app id="inspire" overflow="hidden" >
    <v-navigation-drawer
      v-model="drawer"
      app
      dark
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            Paramètres
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>

      <v-checkbox
      class="pl-3"
      label = "Plein écran"
      v-model="fullScreen"
      @change="toggleFullscreen"
      ></v-checkbox>

      <v-col align="center">
        <v-btn
        depressed
        small
        color="primary"
        @click="resetRGBA()"
        >
          Réinitialiser paramètres
        </v-btn>
      </v-col>

      <v-expansion-panels multiple >

        <v-expansion-panel>
          <v-expansion-panel-header>Tissu sain</v-expansion-panel-header>
          <v-expansion-panel-content>
            <Menue ref="healthy" :red="rgbaHealthy[0]" :green="rgbaHealthy[1]" :blue="rgbaHealthy[2]"  :opacity="rgbaHealthy[3]" addCheckbox="true" @rgba-change="updateHealthy"/>
          </v-expansion-panel-content>

        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Consolidation</v-expansion-panel-header>
          <v-expansion-panel-content>
            <Menue  :red="rbgaConsolidation[0]" :green="rbgaConsolidation[1]" :blue="rbgaConsolidation[2]"  :opacity="rbgaConsolidation[3]" addCheckbox="true" @rgba-change="updateConsolidation"/>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>Verre dépoli</v-expansion-panel-header>
          <v-expansion-panel-content>
              <Menue  :red="rgbaGGO[0]" :green="rgbaGGO[1]" :blue="rgbaGGO[2]"  :opacity="rgbaGGO[3]" addCheckbox="true" @rgba-change="updateGroundGlass"/>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>Arrière-plan</v-expansion-panel-header>
          <v-expansion-panel-content>
              <Menue :red="rgbaBg[0]" :green="rgbaBg[1]" :blue="rgbaBg[2]" opacity="1" addCheckbox="false" @rgba-change="updateBackground"/>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>Camera</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-col align="center">
              <v-btn
              depressed
              small
              color="primary"
              @click="reset()"
              >
                Réinitialiser camera
              </v-btn>
            </v-col>

            <v-col align="center">
              <v-btn
              depressed
              small
              color="primary"
              @click="viewUp()"
              >
                Vue d'en-haut
              </v-btn>
            </v-col>

            <v-col align="center">
              <v-btn
              depressed
              small
              color="primary"
              @click="viewLeft()"
              >
                Vue de gauche
              </v-btn>
            </v-col>

            <v-col align="center">
              <v-btn
              depressed
              small
              color="primary"
              @click="viewRight()"
              >
                Vue de droite
              </v-btn>
            </v-col>

            <v-col align="center">
              <v-btn
              depressed
              small
              color="primary"
              @click="viewFace()"
              >
                Vue d'en face
              </v-btn>
            </v-col>
          </v-expansion-panel-content>
        </v-expansion-panel>

      </v-expansion-panels>
      
    </v-navigation-drawer>
      
    <v-app-bar app  dark  dense>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Visualisation 3D
      </v-toolbar-title>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon 
          small v-bind="attrs"
          v-on="on">
            mdi-information
          </v-icon>
        </template>
        <span>
          Click gauche: Tourner autour de l'axe x et y. <br/>
          Click gauche + CTRL: Tourner autour de l'axe z. <br/>
          Click gauche + SHIFT: Déplacer le modèle. <br/>
          Défiler: zoomer/dézoomer.
        </span>
      </v-tooltip>

      <v-spacer></v-spacer>
      
      <v-file-input class=" pt-6"
        label="Masque"
        outlined
        dense
        accept=".nii.gz"
        ref="mask"
        @change="loadFile"
        @click="fullScreen = false"
      ></v-file-input>

      <v-col align="center">
        <v-btn
        depressed
        color="primary"
        :disabled = "disabled"
        @click="render()"
        >
          Générer
        </v-btn>
      </v-col>
      
      <v-col align="center">
        <v-progress-linear
          v-model= "progress"
          :buffer-value="100"
        ></v-progress-linear>
      </v-col>
      <v-spacer></v-spacer>

      <v-radio-group row v-model="active" class="pt-6" @change="renderTypeChange"
      >
        <v-radio label="Locale"  name="active" :value="0"
        ></v-radio>
        <v-radio label="À Distance" name="active" :value="1"
        ></v-radio>

      </v-radio-group>
    </v-app-bar>
    <v-main>
    </v-main>
  </v-app>
</template>

<script>
  import '@kitware/vtk.js/Rendering/Profiles/Geometry.js';
  import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow.js';
  import vtkActor           from '@kitware/vtk.js/Rendering/Core/Actor.js';
  import vtkMapper          from '@kitware/vtk.js/Rendering/Core/Mapper.js';
  import ImageMarchingCubes from '@kitware/vtk.js/Filters/General/ImageMarchingCubes.js'
  import {readImageFile} from 'itk-wasm';
  import ItkHelper from '@kitware/vtk.js/Common/DataModel/ITKHelper';
  import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader.js';
  import vtkPolyDataNormals from '@kitware/vtk.js/Filters/Core/PolyDataNormals.js'
  import vtkWindowedSincPolyDataFilter from '@kitware/vtk.js/Filters/General/WindowedSincPolyDataFilter.js'
  import Menue from './components/Menue.vue'


  
  //const BACKEND_URL = 'http://127.0.0.1:5000'
  const BACKEND_URL = 'http://193.194.91.207'
  const mapper = vtkMapper.newInstance({
    scalarVisibility : false,
  })
  const mapper2 = vtkMapper.newInstance({
    scalarVisibility : false,
  })
  const mapper3 = vtkMapper.newInstance({
    scalarVisibility : false,
  })
  
  const actor = vtkActor.newInstance({mapper: mapper})
  actor.getProperty().setOpacity(0.2)
  actor.getProperty().setColor(1,0,0)
  
  const actor2 = vtkActor.newInstance({mapper: mapper2})
  actor2.getProperty().setColor(0,1,0)

  const actor3 = vtkActor.newInstance({mapper: mapper3})
  actor3.getProperty().setColor(0,0,1)

  var render, resetCamera, renderer, camera
  //Array(3) [ 186.96521139144897, 224.30427932739258, 1108.8260275788853 ]
  
  export default {
    data: () => 
      ({ 
        active : 1,
        drawer: false ,
        file : null,
        disabled : true,
        progress : 0,
        fullScreen : false,
        rgbaHealthy : [1, 0, 0, 0.2],
        rgbaGGO : [0, 1, 0, 1],
        rbgaConsolidation : [0, 0, 1, 1],
        rgbaBg : [1, 1, 1]
      }),
    components: { Menue },
    mounted() {
      const fullScreenRenderer = vtkFullScreenRenderWindow.newInstance({
        rootContainer: document.querySelector(".v-main")
      });
      renderer = fullScreenRenderer.getRenderer();
      renderer.setBackground(1,1,1)
      const renderWindow = fullScreenRenderer.getRenderWindow();
      resetCamera = renderer.resetCamera;
      camera = renderer.getActiveCamera()
      render = renderWindow.render;
      render()
    },
      
    methods: {
      updateHealthy(r, g, b, a, visible){
        actor.getProperty().setColor(r, g, b)
        actor.getProperty().setOpacity(visible ? a : 0)
        render()
      },
      updateGroundGlass(r, g, b, a, visible){
        actor2.getProperty().setColor(r, g, b)
        actor2.getProperty().setOpacity(visible ? a : 0)
        render()
      },
      updateConsolidation(r, g, b, a, visible){
        actor3.getProperty().setColor(r, g, b)
        actor3.getProperty().setOpacity(visible ? a : 0)
        render()
      },
      updateBackground(r, g, b, a, visible){
        renderer.setBackground(r, g, b)
        render()
      },
      renderTypeChange(){
        if(this.file != null){
          this.disabled = false
          this.progress = 0
          renderer.removeActor(actor)
          renderer.removeActor(actor2)
          renderer.removeActor(actor3)
          render()
        }
      },
      loadFile(file){
        
        this.progress = 0
        this.file = file
        if (file != null){
          if (file.size < 5 * 1000 * 1000){
            this.disabled = false
            renderer.removeActor(actor)
            renderer.removeActor(actor2)
            renderer.removeActor(actor3)
            resetCamera()
            render()
          }
          else{
            this.disabled = true
            alert("Fichier volumineux. Veuillez sélectionnez un fichier approprié.")
          }
        } 
        else{
          this.disabled = true
        }        
      },
      async render(){
        this.disabled = true
        this.progress = 0
        try{
          if (this.active == 1)
            await remoteRender(this)
          else
            await localRender(this)
        }
        catch(err){
          this.progress = 0
          alert("Erreur. Veuillez choisir un autre fichier, ou basculer vers le mode locale.")
        }
          
      },
      reset(){

        resetCamera()
        //console.log(camera.getPosition());
        if (this.active == 1)
          camera.setViewUp(0.008322416371570584, -0.1317329909852448, 0.9912502996074299)
        else
          camera.setViewUp(0.0638390647933373, 0.31043116520380565, -0.9484498223293206)
        
        camera.setPosition(-160.26969938839534, 1130.6042728097786, 242.62245118005765 ) //default 
        render()
      },
      viewUp(){

        resetCamera()
        if (this.active == 1){
          camera.setViewUp(0.008322416371570584, -0.1317329909852448, 0.9912502996074299)
          camera.setPosition(238.98959363178741, 528.6138289062037, 1058.7568450479318)
        }
        else{
          camera.setViewUp(0.0638390647933373, 0.31043116520380565, -0.9484498223293206)
          camera.setPosition(44.684140549930575, 186.02986836678144, -1096.1396679981297) //view up 
        }
        render()
      },
      viewLeft(){
        resetCamera()
        if (this.active == 1)
          camera.setViewUp(0.008322416371570584, -0.1317329909852448, 0.9912502996074299)
        else
          camera.setViewUp(0.0638390647933373, 0.31043116520380565, -0.9484498223293206)
        camera.setPosition(1161.4677353367424, 231.30035610489375, 198.9699476595811) //left view   
        render()
        
      },
      viewRight(){
        resetCamera()
        if (this.active == 1)
          camera.setViewUp(0.008322416371570584, -0.1317329909852448, 0.9912502996074299)
        else
          camera.setViewUp(0.0638390647933373, 0.31043116520380565, -0.9484498223293206)
        camera.setPosition(-782.0226546321263, 344.99119018011845, 158.1968166663067) //right view
        render()
      },
      viewFace(){
        resetCamera()
        if (this.active == 1)
          camera.setViewUp(0.008322416371570584, -0.1317329909852448, 0.9912502996074299)
        else
          camera.setViewUp(0.0638390647933373, 0.31043116520380565, -0.9484498223293206)
        
        camera.setPosition(309.00572637012215, 1185.1632927901624, 258.6694797756485) // face view
        render()
      },
      toggleFullscreen(){
        if (this.fullScreen){
          openFullscreen()
        }
        else{
          closeFullscreen()
        }
      },
      resetRGBA(){
        this.rgbaHealthy = [1, 0, 0, 0.2] 
        this.rgbaGGO = [0, 1, 0, 1]
        this.rbgaConsolidation = [0, 0, 1, 1]
        this.rgbaBg = [1, 1, 1]
        
        actor.getProperty().setOpacity(0.2)
        actor2.getProperty().setOpacity(1)
        actor3.getProperty().setOpacity(1)

        actor.getProperty().setColor(1, 0, 0)
        actor2.getProperty().setColor(0, 1, 0)
        actor3.getProperty().setColor(0, 0, 1)
        renderer.setBackground(1,1,1)

        render()
      }
    }
  }


  async function remoteRender(template){
    const formData = new FormData();
    formData.append('file', template.file);
    let response = await fetch(BACKEND_URL + "/upload/" + template.file.name, 
        {
          method: "POST", 
          body: formData
        });

    
    template.progress = 30
    const dir = await response.text()
    
    const reader = vtkXMLPolyDataReader.newInstance();
    await reader.setUrl(BACKEND_URL + "/download/"+ dir +"/red")  
    template.progress = 45

    const reader2 = vtkXMLPolyDataReader.newInstance();
    await reader2.setUrl(BACKEND_URL + "/download/"+ dir +"/green")
    template.progress = 60

    const reader3 = vtkXMLPolyDataReader.newInstance();
    await reader3.setUrl(BACKEND_URL + "/download/"+ dir +"/blue")
    template.progress = 75


    const smoothFilter = vtkWindowedSincPolyDataFilter.newInstance({
      numberOfIterations: 7,
      passBand : 0.01,
    })
    const smoothFilter2 = vtkWindowedSincPolyDataFilter.newInstance({
      numberOfIterations: 7,
      passBand : 0.01,
    })
    const smoothFilter3 = vtkWindowedSincPolyDataFilter.newInstance({
      numberOfIterations: 7,
      passBand : 0.01,
    })  

    const normals = vtkPolyDataNormals.newInstance()
    const normals2 = vtkPolyDataNormals.newInstance()
    const normals3 = vtkPolyDataNormals.newInstance()

    smoothFilter.setInputConnection(reader.getOutputPort())
    smoothFilter2.setInputConnection(reader2.getOutputPort())
    smoothFilter3.setInputConnection(reader3.getOutputPort())

    normals.setInputConnection(smoothFilter.getOutputPort())
    normals2.setInputConnection(smoothFilter2.getOutputPort())
    normals3.setInputConnection(smoothFilter3.getOutputPort())

    mapper.setInputConnection(normals.getOutputPort());
    mapper.update()
    //actor.getProperty().setColor(1,0,0)
    renderer.addActor(actor);

    mapper2.setInputConnection(normals2.getOutputPort());
    mapper2.update()
    //actor2.getProperty().setColor(0,1,0)
    renderer.addActor(actor2);  

    mapper3.setInputConnection(normals3.getOutputPort());
    mapper3.update()
    //actor3.getProperty().setColor(0,0,1)
    renderer.addActor(actor3);
    template.progress = 90
    
    camera.setViewUp(0.008322416371570584, -0.1317329909852448, 0.9912502996074299)
    camera.setPosition(-160.26969938839534, 1130.6042728097786, 242.62245118005765 ) 
    resetCamera()
    render()  
    template.progress = 100
  }


  async function localRender(template) {
    template.progress = 10
    const {image, _} = await readImageFile(null,template.file);
    template.progress = 20
    
    const marchingCubes = ImageMarchingCubes.newInstance({
      contourValue : 1,
    })
    const marchingCubes2 = ImageMarchingCubes.newInstance({
      contourValue : 2
    })
    const marchingCubes3 = ImageMarchingCubes.newInstance({
      contourValue : 3
    })
    
    marchingCubes.setInputData(ItkHelper.convertItkToVtkImage(image))

    marchingCubes2.setInputData(ItkHelper.convertItkToVtkImage(image))

    marchingCubes3.setInputData(ItkHelper.convertItkToVtkImage(image))

    mapper.setInputConnection(marchingCubes.getOutputPort())
    mapper.update()
    template.progress = 40

    mapper2.setInputConnection(marchingCubes2.getOutputPort())
    mapper2.update()
    template.progress = 60

    mapper3.setInputConnection(marchingCubes3.getOutputPort())
    mapper3.update()
    template.progress = 80

    // actor.getProperty().setColor(1,0,0)
    // actor2.getProperty().setColor(0,1,0)
    // actor3.getProperty().setColor(0,0,1)
    renderer.addActor(actor)
    renderer.addActor(actor2)
    renderer.addActor(actor3)
    
    camera.setViewUp(0.0638390647933373, 0.31043116520380565, -0.9484498223293206)
    camera.setPosition(-160.26969938839534, 1130.6042728097786, 242.62245118005765 ) 
    resetCamera()
    render()
    template.progress = 100
}

function openFullscreen() {
  const doc = document.documentElement;
  if (doc.requestFullscreen) {
    doc.requestFullscreen();
  } else if (doc.webkitRequestFullscreen) { /* Safari */
    doc.webkitRequestFullscreen();
  } else if (doc.msRequestFullscreen) { /* IE11 */
    doc.msRequestFullscreen();
  }
}

/* Close fullscreen */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.webkitExitFullscreen) { /* Safari */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE11 */
    document.msExitFullscreen();
  }
}
//
</script>

<style>
html { overflow-y: auto }

/* ::-webkit-scrollbar{
  width: 10 ;
} */

</style>

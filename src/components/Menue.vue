<template>
  <div>
    <v-checkbox
    v-if="addCheckbox == 'true'"
    label = "Afficher"
    @change="toggleDisplay"
    input-value="true"
    ></v-checkbox>
    <v-slider
      v-if="addCheckbox == 'true'"
      label="Opacité"
      max="1"
      min="0"
      step = "0.05"
      color="white"
      :disabled = "disabled"
      v-model="opacity"
      @input="rgbaChange"
    ></v-slider>
    <v-slider
      label="R"
      max="1"
      min="0"
      step = "0.01"
      color="red"
      v-model = "red"
      :disabled = "disabled"
      @input="rgbaChange"
    ></v-slider>
    <v-slider
      label="G"
      max="1"
      min="0"
      step = "0.01"
      color="green"
      v-model = "green"
      :disabled = "disabled"
      @input="rgbaChange"
    ></v-slider>
    <v-slider
      label="B"
      max="1"
      min="0"
      step = "0.01"
      color="blue"
      v-model = "blue"
      :disabled = "disabled"
      @input="rgbaChange"
       
    ></v-slider>
  </div>
    
</template>

<script>
  export default {
    name: 'Menue',
    props : ["red", "green", "blue", "opacity", "addCheckbox"],
    data: () => ({ 
      disabled: false
      }),
    methods: {
      rgbaChange(value){
        this.$emit("rgba-change", this.red, this.green, this.blue, this.opacity, !(this.disabled))
      },
      toggleDisplay(){
        this.disabled = !this.disabled
        this.$emit("rgba-change", this.red, this.green, this.blue, this.opacity, !(this.disabled))
      }
    }
    
  }
</script>
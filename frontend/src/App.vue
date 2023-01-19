<template>
    <div id="app">
      <el-menu
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <li id="navi-title">GridLayout</li>
      </el-menu>
      <svg width="0" height="0">
          <defs id="texture">
              <pattern v-for="(texture, i) in textures" v-html="texture" :key="i">
              </pattern>
          </defs>
      </svg>
      <data-view></data-view>
    </div>
  </template>

<script>
/* eslint-disable max-len */
import DataView from './components/DataView.vue';
import Vue from 'vue';
import {Menu, MenuItem} from 'element-ui';
import axios from 'axios';
import {simulatedAnnealing2FindBestPalette, evaluatePalette} from './js/optimizeFunc';

Vue.use(Menu);
Vue.use(MenuItem);

// main vue component
export default {
    name: 'App',
    components: {DataView},
    data:
          function() {
              return {
                  textures: [],
                  colorsscope: {'hue_scope': [0, 360], 'lumi_scope': [35, 95]},
              };
          },
    mounted: function() {
        const store = this.$store;
        const that = this;
        axios.get(store.getters.URL_GET_ALL_DATA)
            .then(function(response) {
                store.commit('setAllData', response.data);
                console.log('network data', store.getters.network);
            });
        axios.post(store.getters.URL_GET_LABEL_HIERARCHY)
            .then(function(response) {
                const matrix = response.data;
                const colors = that.initColor(matrix.hierarchy);
                store.commit('setColors', colors);
                // init hierarchy colors
                const hierarchyColors = {...colors};
                store.commit('setHierarchyColors', hierarchyColors);
                // save label hierarchy data
                store.commit('setLabelHierarchy', matrix);
                console.log('label hierarchy data', matrix);
            });
    },
    methods: {
        initColor(hierarchy) {
            const basecolors = ['#8dd3c7', '#fee789', '#fe614f', '#80b1d3',
                '#fdb462', '#b3de69', '#fccde5', '#bc80bd', '#ccebc5', '#ffed6f'];
            // 1:ffffb3  2:fb8072
            const colors = {}; // fill and opacity

            for (let i=0; i<hierarchy.length; i++) {
                colors[hierarchy[i].name] = {
                    fill: basecolors[i],
                    opacity: 1,
                };
            }
            return colors;
        },
        rgb2hex(rgb) {
            return '#'+(1<<24|rgb.r<<16|rgb.g<<8|rgb.b).toString(16).substring(1);
        },
    },
};

</script>

<style>
html, body, #app {
  margin: 0;
  width: 100%;
  height: 100%;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

#navigation {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  background: rgb(54, 54, 54);
}

#navi-title {
  color: rgb(255, 255, 255);
  font-weight: 900;
  font-size: 40px;
  margin: 0 50px 0 20px;
  float: left;
}
</style>


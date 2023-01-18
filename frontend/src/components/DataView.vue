<template>
    <div id="data-content">
        <gird-layout ref="grider"></gird-layout>
        <legend-component></legend-component>
    </div>
</template>

<script>
import GirdLayout from './GridLayout.vue';
import LegendComponent from './Legend.vue';

export default {
    components: {GirdLayout, LegendComponent},
    name: 'DataView',
    data() {
        return {
            hoveredNode: [],
        };
    },
    methods: {
    },
};
</script>

<style scoped>
#data-content {
    width: 100%;
    height: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
}
</style>

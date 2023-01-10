import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        APIBASE: BACKEND_BASE_URL,
        network: {},
        statistic: {
            'loss': [],
            'accuracy': [],
            'recall': [],
        },
        labelHierarchy: [],
        labelnames: [],
        layoutInfo: {
            layoutNetwork: {}, // very similar to allData.network, with some attributes for layout added
            focusID: '_model/', // default focus node is root node
            t: -1, // a timestamp
        },
        colors: {},
        hierarchyColors: {},
        featureMapNodeID: null, // which node to show feature map
    },
    mutations: {
        setAllData(state, allData) {
            state.network = allData.network;
            state.statistic = allData.statistic;
        },
        setNetwork(state, network) {
            state.network = network;
        },
        setLayoutInfo(state, layoutInfo) {
            state.layoutInfo = layoutInfo;
        },
        setFeatureMapNodeID(state, featureMapNodeID) {
            state.featureMapNodeID = featureMapNodeID;
        },
        setLabelHierarchy(state, hierarchy) {
            state.labelHierarchy = hierarchy.hierarchy;
            state.labelnames = hierarchy.names;
        },
        setColors(state, colors) {
            state.colors = colors;
        },
        setSelectedImageID(state, selectedImageID) {
            state.selectedImageID = selectedImageID;
        },
        setHierarchyColors(state, hierarchyColors) {
            state.hierarchyColors = hierarchyColors;
        },
    },
    getters: {
        network: (state) => state.network,
        statistic: (state) => state.statistic,
        featureMapNodeID: (state) => state.featureMapNodeID,
        selectedImageID: (state) => state.selectedImageID,
        layoutInfo: (state) => state.layoutInfo,
        labelHierarchy: (state) => state.labelHierarchy,
        labelnames: (state) => state.labelnames,
        colors: (state) => state.colors,
        hierarchyColors: (state) => state.hierarchyColors,
        URL_GET_ALL_DATA: (state) => state.APIBASE + '/api/allData',
        URL_GET_FEATURE_INFO: (state) => state.APIBASE + '/api/featureInfo',
        URL_GET_LABEL_HIERARCHY: (state) => state.APIBASE + '/api/labelHierarchy',
        URL_GET_FEATURE: (state) => {
            return (leafID, index) => state.APIBASE + `/api/feature?leafID=${leafID}&index=${index}`;
        },
        URL_GET_IMAGE_GRADIENT: (state) => {
            return (imageID, method) => state.APIBASE + `/api/imageGradient?imageID=${imageID}&method=${method}`;
        },
        URL_GET_GRID: (state) => state.APIBASE + '/api/grid',
        URL_FIND_GRID_PARENT: (state) => state.APIBASE + '/api/findParent',
        URL_RUN_IMAGE_ON_MODEL: (state) => state.APIBASE + '/api/networkOnImage',
    },
});

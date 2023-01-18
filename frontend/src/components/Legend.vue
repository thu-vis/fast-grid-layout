<template>
    <svg id="legend-drawer">
        <g id="legend-g"></g>
    </svg>
</template>

<script>
import {mapGetters} from 'vuex';
import * as d3 from 'd3';

export default {
    name: 'legend',
    computed: {
        ...mapGetters([
            'hierarchyColors',
            'labelnames',
        ]),
        legendG: function() {
            return d3.select('#legend-drawer').select('#legend-g');
        },
    },
    data: function() {
        return {
            legendsInG: undefined,
        };
    },
    watch: {
        // all info was loaded
        hierarchyColors: function(newColors, oldColors) {
            this.render();
        },
    },
    methods: {
        render: function() {
            this.legendsInG = this.legendG.selectAll('.legend-row').data(this.labelnames, (d)=>d);
            const legendsInG = this.legendsInG.enter().append('g')
                .attr('class', 'legend-row')
                .attr('transform', (d, i)=>`translate(10, ${i*25+100})`);
            legendsInG.append('rect')
                .attr('x', 0)
                .attr('y', 0)
                .attr('width', 18)
                .attr('height', 18)
                .attr('stroke-width', 0)
                .attr('fill', (d)=>this.hierarchyColors[d].fill)
                .attr('opacity', (d)=>this.hierarchyColors[d].opacity);

            legendsInG.append('text')
                .attr('x', 25)
                .attr('y', 15)
                .attr('font-size', 15)
                .attr('font-weight', 'bold')
                .attr('color', 'gray')
                .text((d)=>d);
        },
    },
};
</script>

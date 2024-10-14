import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './IdeaGraph.css';

const IdeaGraph = ({ ideas, links }) => {
    const svgRef = useRef(null);

    const drawGraph = () => {
        const width = 960;
        const height = 600;

        d3.select(svgRef.current).selectAll('*').remove();

        const svg = d3.select(svgRef.current)
                      .attr('width', width)
                      .attr('height', height);

        const simulation = d3.forceSimulation(ideas)
                             .force('link', d3.forceLink(links).id(d => d.id))
                             .force('charge', d3.forceManyBody())
                             .force('center', d3.forceCenter(width / 2, height / 2));

        const link = svg.append('g')
                        .attr('stroke', '#999')
                        .attr('stroke-opacity', 0.6)
                        .selectAll('line')
                        .data(links)
                        .join('line')
                        .attr('stroke-width', d => Math.sqrt(d.value));

        const node = svg.append('g')
                        .attr('stroke', '#fff')
                        .attr('stroke-width', 1.5)
                        .selectAll('circle')
                        .data(ideas)
                        .join('circle')
                        .attr('r', 5)
                        .attr('fill', colorByGroup)
                        .call(drag(simulation));

        const label = svg.append("g")
                         .attr("class", "labels")
                         .selectAll("text")
                         .data(ideas)
                         .enter().append("text")
                         .attr("dx", 8)
                         .attr("dy", "0.35em")
                         .text(d => d.name);

        simulation.on('tick', () => {
            link.attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            node.attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            label.attr("x", d => d.x)
                 .attr("y", d => d.y);
        });

        function colorByGroup(d) {
            return d.group === 1 ? '#ff4136' : '#0074D9';
        }

        function drag(simulation) {
            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }

            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }

            return d3.drag()
                     .on('start', dragstarted)
                     .on('drag', dragged)
                     .on('end', dragended);
        }
    };

    useEffect(drawGraph, [ideas, links]);

    return <svg ref={svgRef}></svg>;
};

export default IdeaGraph;
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './IdeaGraph.css';

const IdeaGraph = ({ fetchData }) => {
    const svgRef = useRef(null);

    useEffect(() => {
        const updateGraphWithData = async () => {
            const graphData = await fetchData();
            const { ideas, links } = graphData;
            if (ideas.length === 0 || links.length === 0) {
                return;
            }

            const svgElement = d3.select(svgRef.current);
            // Clear existing SVG content to ensure a fresh graph.
            svgElement.selectAll('*').remove();

            // Graph dimensions, consider making these dynamic or props.
            const graphWidth = 960;
            const graphHeight = 600;
        };

        updateGraphWithData();
    }, [fetchData]);

    return <svg ref={svgRef}></svg>;
};

export default IdeaGraph;
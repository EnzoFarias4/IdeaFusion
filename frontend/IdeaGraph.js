import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './IdeaGraph.css';

const IdeaGraph = ({ fetchData }) => {
    const svgRef = useRef(null);

    useEffect(() => {
        const getDataAndUpdateGraph = async () => {
            const { ideas, links } = await fetchData();
            if (!ideas.length || !links.length) return;

            const svg = d3.select(svgRef.current);
            svg.selectAll('*').remove();

            const width = 960;
            const height = 600;
        };

        getDataAndUpdateGraph();
    }, [fetchData]);

    return <svg ref={svgRef}></svg>;
};

export default IdeaGraph;
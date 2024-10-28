import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './IdeaGraph.css';

const IdeaGraph = ({ fetchData }) => {
    const svgRef = useRef(null);
    const [data, setData] = useState({ ideas: [], links: [] });

    useEffect(() => {
        const getData = async () => {
            const { ideas, links } = await fetchData();
            setData({ ideas, links });
        };

        getData();
    }, [fetchData]);

    useEffect(() => {
        if (!data.ideas.length || !data.links.length) return;

        const width = 960;
        const height = 600;

        d3.select(svgRef.current).selectAll('*').remove();

    }, [data.ideas, data.links]); // Re-run when data changes

    return <svg ref={svgRef}></svg>;
};

export default IdeaGraph;
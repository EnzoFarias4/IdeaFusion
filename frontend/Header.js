// ErrorBoundary.js
import React, { Component } from 'react';

class ErrorBoundaryWrapper extends Component {
    constructor(props) {
        super(props);
        this.state = { hasEncounteredError: false };
    }

    static getErrorStateFromError(error) {
        return { hasEncounteredError: true };
    }

    catchErrorDetails(error, errorInfo) {
        console.log(error, errorInfo);
    }

    render() {
        if (this.state.hasEncounteredError) {
            return <h1>Oops, something went wrong.</h1>;
        }

        return this.props.children; 
    }
}

export default ErrorBoundaryWrapper;

// Header.js
import React from 'react';
import ErrorBoundaryWrapper from './ErrorBoundaryWrapper';
import { Link } from 'react-router-dom';

const NavigationHeader = () => {
    return (
        <ErrorBoundaryWrapper>
            <header>
                <nav>
                    <ul>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                            <Link to="/about">About</Link>
                        </li>
                        <li>
                            <Link to="/projects">Projects</Link>
                        </li>
                        <li>
                            <Link to="/contact">Contact</Link>
                        </li>
                    </ul>
                </nav>
            </header>
        </ErrorBoundaryWrapper>
    );
};

export default NavigationHeader;
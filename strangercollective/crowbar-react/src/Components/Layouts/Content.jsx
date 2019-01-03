import React, { Component } from 'react';

import CharacterPage from '../Pages/CharacterPage'

class Content extends Component {
  render() {
    return (
      <div className="content layout">
      <div className="content wrapper">
      <CharacterPage />
      </div>
      </div>
    );
  }
}

export default Content;

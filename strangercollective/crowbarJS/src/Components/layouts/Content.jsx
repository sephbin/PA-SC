import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import AttributeCard from '../AttributeCard'
import TraitCard from '../TraitCard'
import SkillCard from '../SkillCard'
import CultureCard from '../CultureCard'
import PossesionCard from '../PossesionCard'
import LanguageCard from '../LanguageCard'
import MainCard from '../MainCard'
import CharacterPage from '../pages/CharacterPage'
import CharacterList from '../pages/CharacterList'

class Content extends Component {
  render() {
  	const style = {
	position: 'fixed',
	bottom: this.props.json.layout.universal.sideWidth,
	left: this.props.json.layout.universal.sideWidth,
	right: this.props.json.layout.universal.sideWidth,
	top: this.props.json.layout.universal.sideWidth,
	backgroundColor: '#111',
	padding: 8,
  overflowX: 'hidden',
  overflowY: 'hidden',
  // overflowY: 'auto',
};

    return (
      <div style={style}>
      {this.props.json.page === "CharacterList" && (
      <CharacterList json={this.props.json} func={this.props.func} />
        )}
      {this.props.json.page === "CharacterPage" && (
      <CharacterPage json={this.props.json} />
      )}
      </div>
    );
  }
}

export default Content;

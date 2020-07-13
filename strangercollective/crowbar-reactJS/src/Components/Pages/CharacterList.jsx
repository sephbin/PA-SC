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


class CharacterList extends Component {
  render() {

    return (
      <div>
{this.props.json.characterList.map( (sk, i) => {
  return (
    <Card id={(sk.id)} key={(sk.id)} onClick={() => this.props.func(sk.id) } >{sk.name}</Card>
  )
})}
      </div>
    );
  }
}
export default CharacterList;



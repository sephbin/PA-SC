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
import RangedCard from '../RangedCard'
import MeleeCard from '../MeleeCard'
import LanguageCard from '../LanguageCard'
import MainCard from '../MainCard'


class CharacterPage extends Component {
  render() {

    return (
      <Grid container spacing={"8"} style={{height:"100%"}}>
        <Grid item xs={3}>
          <AttributeCard json={this.props.json.character} />
          <TraitCard cardTitle="Advantages" json={this.props.json.character.advantages} />
          <TraitCard cardTitle="Disadvantages" json={this.props.json.character.disadvantages} />
          <SkillCard json={this.props.json.character.skills} />
        </Grid>
        <Grid item xs={6}>
          <MainCard json={this.props.json.character} />
        </Grid>
        <Grid item xs ={3}>
          <LanguageCard json={this.props.json.character.languages} />
          <CultureCard json={this.props.json.character} />
          <MeleeCard json={this.props.json.character.melee} />
          <RangedCard json={this.props.json.character.ranged} />
          <PossesionCard json={this.props.json.character.possessions} char={this.props.json.character} />
        </Grid>
      </Grid>
    );
  }
}
export default CharacterPage;



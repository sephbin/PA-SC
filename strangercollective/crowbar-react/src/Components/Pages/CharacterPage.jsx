import React, { Component, Fragment } from 'react';
import CharacterCard from '../Cards/CharacterCard';
import AttributeCard from '../Cards/AttributeCard';
// import TraitCard from '../Cards/TraitCard';
// import SkillCard from '../Cards/SkillCard';
// import CultureCard from '../Cards/CultureCard';
// import PossesionCard from '../Cards/PossesionCard';
// import RangedCard from '../Cards/RangedCard';
// import MeleeCard from '../Cards/MeleeCard';
// import LanguageCard from '../Cards/LanguageCard';
import MainCard from '../Cards/MainCard';
import '../Cards/Cards.css';

class CharacterPage extends Component {
  render() {

    return (
      <Fragment>
      <div className="left column">
      <div className="column wrapper">
          <CharacterCard/>
          <AttributeCard/>
          {/*<TraitCard cardTitle="Advantages" json={this.props.json.character.reladvantage} />*/}
          {/*<TraitCard cardTitle="Disadvantages" json={this.props.json.character.reldisadvantage} />*/}
          {/*<SkillCard json={this.props.json.character.relskill} />*/}
        </div>
        </div>

        <div className="center column">
        <div className="column wrapper">
          <MainCard/>
        </div>
        </div>
        <div className="right column">
        <div className="column wrapper">
          {/*<LanguageCard json={this.props.json.character.languages} />*/}
          {/*<CultureCard json={this.props.json.character} />*/}
          {/*<MeleeCard json={this.props.json.character.relpossession} />*/}
          {/*<RangedCard json={this.props.json.character.relpossession} />*/}
          {/*<PossesionCard json={this.props.json.character.relpossession} char={this.props.json.character} />*/}
        </div>
        </div>
        </Fragment>
    );
  }
}
export default CharacterPage;



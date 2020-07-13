import React, { Component, Fragment } from 'react';
import CharacterCard from '../Cards/CharacterCard';
import AttributeCard from '../Cards/AttributeCard';
import TraitCard from '../Cards/TraitCard';
import SkillCard from '../Cards/SkillCard';
// import CultureCard from '../Cards/CultureCard';
import MeleeCard from '../Cards/MeleeCard';
import RangedCard from '../Cards/RangedCard';
import PossesionCard from '../Cards/PossesionCard';
// import LanguageCard from '../Cards/LanguageCard';
import MainCard from '../Cards/MainCard';
import PossessionModal from '../Modals/PossessionModal';
import AdvantageModal from '../Modals/AdvantageModal';
import '../Cards/Cards.css';
import '../Modals/Modals.css';

class CharacterPage extends Component {
  render() {

    return (
      <Fragment>
      <div className="left column">
      <div className="column wrapper">
          <CharacterCard/>
          <AttributeCard/>
          <TraitCard cardTitle="Advantages" cardArray="reladvantage" />
          <TraitCard cardTitle="Disadvantages" cardArray="reldisadvantage" />
          <SkillCard />
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
          <MeleeCard />
          <RangedCard />
          <PossesionCard />
        </div>
        </div>
      {/*MODALS*/}
      <PossessionModal />
      <AdvantageModal />
        </Fragment>
    );
  }
}
export default CharacterPage;



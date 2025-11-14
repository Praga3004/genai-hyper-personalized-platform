import React, {useState} from "react";
import { View, Text, StyleSheet, ScrollView} from 'react-native';
import FilterBar from "../components/FilterBar";
import PeopleList from "../components/PeopleList";
import GenerateContentButton from "../components/GenerateContentButton";
import {peopleData} from "../data/peopleData";

export default function PeopleDirectory(){
    const [ selectedPeople, setSelectedPeople]= useState();
    const [filters, setFilters]= useState({ age: 'ALL', gender: 'ALL', location: 'ALL'});

    const toggleSelect = (id)=> {
        setSelectedPeople(prev => prev.includes(id)? prev.filter(pid=>pid !==id) : [...prev, id]);

    };

    return (
        <ScrollView style={styles.container}>
            <Text style={styles.header}>People Directory</Text>
            <FilterBar filters={filters} setFilters={setFilters}></FilterBar>
            <PeopleList data={peopleData} selected={selectedPeople} toggleSelect={toggleSelect}/>
            { selectedPeople.length > 0 && (<GenerateContentButton selectedPeople={selectedPeople}/>)}
            
        </ScrollView>

    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,padding: 20, backgroundColor: '#f5f5f5'},
        header: {fontSize: 24, fontWeight: 'bold', marginBottom: 20,}
    });
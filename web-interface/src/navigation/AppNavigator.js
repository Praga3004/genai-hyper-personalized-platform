import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import PeopleDirectory from '../pages/PeopleDirectory';
import PersonDetails from '../pages/PersonDetails';

const Stack = createStackNavigator();

export default function AppNavigator() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Directory">
                <Stack.Screen 
                    name="PeopleDirectory"
                    component={PeopleDirectory} options={{ title: 'People Directory' }} />
                <Stack.Screen 
                    name="PersonDetails"
                    component={PersonDetails} options={{ title: 'Person Details' }} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
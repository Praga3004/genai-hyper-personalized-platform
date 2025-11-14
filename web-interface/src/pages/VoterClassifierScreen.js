import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator
} from "react-native";
import { Picker } from "@react-native-picker/picker"; 
import { classifyVoterProfile } from "../api/voterApi";

export default function VoterClassifierScreen() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("Male");
  const [location, setLocation] = useState("Coimbatore");
  const [voterHistory, setVoterHistory] = useState("First-time voter");
  const [interests, setInterests] = useState("");
  const [painPoints, setPainPoints] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const onSubmit = async () => {
    setError("");
    setResult(null);

    if (!age || isNaN(Number(age))) {
      setError("Age is required and must be a number");
      return;
    }

    const profile = {
      name: name || "Unnamed",
      age: Number(age),
      gender,
      location,
      voter_history: voterHistory,
      interests: interests
        .split(",")
        .map((v) => v.trim())
        .filter(Boolean),
      pain_points: painPoints
        .split(",")
        .map((v) => v.trim())
        .filter(Boolean)
    };

    try {
      setLoading(true);
      const res = await classifyVoterProfile(profile);
      setResult(res);
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Voter Category Classifier</Text>
      <Text style={styles.subtitle}>
        Enter voter details. Backend uses VDB + OpenAI to map to{" "}
        <Text style={{ fontWeight: "bold" }}>
          first-time / apathetic / swing / women / senior
        </Text>{" "}
        categories.
      </Text>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      {/* Name */}
      <View style={styles.field}>
        <Text style={styles.label}>Name</Text>
        <TextInput
          style={styles.input}
          value={name}
          onChangeText={setName}
          placeholder="e.g., Arun Kumar"
        />
      </View>

      {/* Age */}
      <View style={styles.field}>
        <Text style={styles.label}>Age</Text>
        <TextInput
          style={styles.input}
          value={age}
          onChangeText={setAge}
          placeholder="19"
          keyboardType="numeric"
        />
      </View>

      {/* Gender */}
      <View style={styles.field}>
        <Text style={styles.label}>Gender</Text>
        <View style={styles.pickerWrapper}>
          <Picker selectedValue={gender} onValueChange={(v) => setGender(v)}>
            <Picker.Item label="Male" value="Male" />
            <Picker.Item label="Female" value="Female" />
            <Picker.Item label="Other" value="Other" />
          </Picker>
        </View>
      </View>

      {/* Location */}
      <View style={styles.field}>
        <Text style={styles.label}>Location (City / Town)</Text>
        <TextInput
          style={styles.input}
          value={location}
          onChangeText={setLocation}
          placeholder="e.g., Coimbatore, Madurai"
        />
      </View>

      {/* Voter history */}
      <View style={styles.field}>
        <Text style={styles.label}>Voter History</Text>
        <View style={styles.pickerWrapper}>
          <Picker
            selectedValue={voterHistory}
            onValueChange={(v) => setVoterHistory(v)}
          >
            <Picker.Item label="First-time voter" value="First-time voter" />
            <Picker.Item
              label="Rarely votes"
              value="Rarely votes"
            />
            <Picker.Item
              label="Regular voter"
              value="Regular voter"
            />
            <Picker.Item
              label="Non-voter in last 2 elections"
              value="Non-voter in last 2 elections"
            />
          </Picker>
        </View>
      </View>

      {/* Interests */}
      <View style={styles.field}>
        <Text style={styles.label}>Interests (comma separated)</Text>
        <TextInput
          style={[styles.input, styles.multiline]}
          value={interests}
          onChangeText={setInterests}
          placeholder="technology, jobs, college, women safety"
          multiline
        />
      </View>

      {/* Pain points */}
      <View style={styles.field}>
        <Text style={styles.label}>Pain Points (comma separated)</Text>
        <TextInput
          style={[styles.input, styles.multiline]}
          value={painPoints}
          onChangeText={setPainPoints}
          placeholder="unemployment, transport safety, bad roads"
          multiline
        />
      </View>

      {/* Submit button */}
      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={onSubmit}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Classify & Generate Campaign</Text>
        )}
      </TouchableOpacity>

      {/* Result */}
      {result && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>Result</Text>
          <Text style={styles.resultLine}>
            Category:{" "}
            <Text style={styles.categoryText}>{result.category}</Text>
          </Text>
          {typeof result.confidence === "number" && (
            <Text style={styles.resultLine}>
              Confidence: {(result.confidence * 100).toFixed(1)}%
            </Text>
          )}
          {result.personalized_campaign && (
            <>
              <Text style={styles.sectionHeader}>Personalized Campaign</Text>
              {result.personalized_campaign.sms_tamil && (
                <View style={styles.block}>
                  <Text style={styles.blockLabel}>SMS (Tamil)</Text>
                  <Text style={styles.blockBody}>
                    {result.personalized_campaign.sms_tamil}
                  </Text>
                </View>
              )}
              {result.personalized_campaign.image_prompt && (
                <View style={styles.block}>
                  <Text style={styles.blockLabel}>Image Prompt</Text>
                  <Text style={styles.blockBody}>
                    {result.personalized_campaign.image_prompt}
                  </Text>
                </View>
              )}
              {result.personalized_campaign.audio_prompt && (
                <View style={styles.block}>
                  <Text style={styles.blockLabel}>Audio Prompt</Text>
                  <Text style={styles.blockBody}>
                    {result.personalized_campaign.audio_prompt}
                  </Text>
                </View>
              )}
            </>
          )}
        </View>
      )}

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: "#f5f5f5"
  },
  title: {
    fontSize: 22,
    fontWeight: "700",
    marginBottom: 4
  },
  subtitle: {
    fontSize: 13,
    color: "#4b5563",
    marginBottom: 12
  },
  error: {
    color: "#b91c1c",
    marginBottom: 8
  },
  field: {
    marginBottom: 12
  },
  label: {
    fontSize: 13,
    color: "#4b5563",
    marginBottom: 4
  },
  input: {
    backgroundColor: "#fff",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#e5e7eb",
    paddingHorizontal: 10,
    paddingVertical: 8,
    fontSize: 14
  },
  multiline: {
    height: 70,
    textAlignVertical: "top"
  },
  pickerWrapper: {
    backgroundColor: "#fff",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#e5e7eb"
  },
  button: {
    backgroundColor: "#0f172a",
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: "center",
    marginTop: 8
  },
  buttonDisabled: {
    opacity: 0.7
  },
  buttonText: {
    color: "#fff",
    fontWeight: "700"
  },
  resultCard: {
    marginTop: 16,
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: "#e5e7eb"
  },
  resultTitle: {
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 4
  },
  resultLine: {
    fontSize: 14,
    marginBottom: 4
  },
  categoryText: {
    fontWeight: "700"
  },
  sectionHeader: {
    marginTop: 8,
    fontSize: 14,
    fontWeight: "700"
  },
  block: {
    marginTop: 6
  },
  blockLabel: {
    fontSize: 13,
    fontWeight: "600",
    marginBottom: 2
  },
  blockBody: {
    fontSize: 13,
    color: "#374151"
  }
});

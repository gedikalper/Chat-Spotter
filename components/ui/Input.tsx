// components/ui/input.tsx

import { Ionicons } from "@expo/vector-icons";
import React, { useState } from "react";
import { Text, TextInput, TextInputProps, TouchableOpacity, View } from "react-native";

type InputProps = {
  label?: string;
  icon?: keyof typeof Ionicons.glyphMap;
  secure?: boolean;
  showPasswordToggle?: boolean;
} & TextInputProps;

export const Input = ({
  label,
  icon,
  secure,
  showPasswordToggle,
  ...textInputProps
}: InputProps) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const isSecure = secure || textInputProps.secureTextEntry;

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  return (
    <View className="w-full">
      {label && (
        <Text className="text-gray-700 mb-2 text-base font-medium">{label}</Text>
      )}
      <View className="flex-row items-center bg-white border border-gray-200 rounded-lg px-4 py-1 mb-3">
        {icon && <Ionicons name={icon} size={20} color="#6B7280" style={{ marginRight: 8 }} />}
        <TextInput
          className="flex-1 text-gray-900 text-base"
          placeholderTextColor="#9CA3AF"
          secureTextEntry={isSecure && !isPasswordVisible}
          {...textInputProps}
        />
        {showPasswordToggle && isSecure && (
          <TouchableOpacity onPress={togglePasswordVisibility}>
            <Ionicons 
              name={isPasswordVisible ? "eye-off-outline" : "eye-outline"} 
              size={20} 
              color="#6B7280" 
            />
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};
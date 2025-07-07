// components/ui/PageWrapper.tsx

import React from "react";
import { Text, View } from "react-native";

type Props = {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
};

export default function PageWrapper({ title, subtitle, children }: Props) {
  return (
    <View className="flex-1 bg-white px-6 justify-center">
      <View className="mb-10">
        <Text className="text-3xl font-bold text-green-700 text-center">{title}</Text>
        {subtitle && (
          <Text className="text-base text-green-700 text-center mt-2">
            {subtitle}
          </Text>
        )}
      </View>
      <View className="space-y-4">{children}</View>
    </View>
  );
}

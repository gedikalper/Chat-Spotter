// components/ui/Page.tsx
import React, { ReactNode } from "react";
import { ImageBackground, SafeAreaView, ScrollView, StatusBar, View } from "react-native";

interface PageProps {
  children: ReactNode;
  scrollable?: boolean;
  className?: string;
}

export const Page = ({ children, scrollable = true, className = "" }: PageProps) => {
  const content = (
    <ImageBackground
      source={require("@/assets/images/grid.png")}
      resizeMode="cover"
      className={`flex-1`}
      // style={{ backgroundColor: colors.primary }}
    >
      <StatusBar barStyle="light-content" backgroundColor="#1abc9c" />
      {scrollable ? (
        <ScrollView contentContainerStyle={{ flexGrow: 1 }}>{children}</ScrollView>
      ) : (
        <View className="flex-1">{children}</View>
      )}
    </ImageBackground>
  );

  return (
    <SafeAreaView className="flex-1 bg-[#122414]">{content}</SafeAreaView>
  );
};
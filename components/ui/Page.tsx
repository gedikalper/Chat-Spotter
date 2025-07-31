import Constants from "expo-constants";
import { useColorScheme } from "nativewind";
import React, { ReactNode } from "react";
import { ScrollView, StatusBar, View } from "react-native";

interface PageProps {
  children: ReactNode;
  scrollable?: boolean;
  className?: string;
}

const STATUS_BAR_HEIGHT = Constants.statusBarHeight;
const IS_IOS = Constants.platform?.ios;

export const Page = ({
  children,
  scrollable = false,
  className = "",
}: PageProps) => {
  const { colorScheme } = useColorScheme();
  const isDark = colorScheme === "dark";

  // Content render fonksiyonu
  const renderContent = () => {
    if (scrollable) {
      return (
        <ScrollView
          contentContainerStyle={{ flexGrow: 1 }}
          showsVerticalScrollIndicator={false}
        >
          {children}
        </ScrollView>
      );
    }

    return <View className="flex-1">{children}</View>;
  };

  return (
    <View className={`flex-1 px-safe-offset-5 bg-white pt-[20px] ${className}`}>
      <View className="flex-1">
        <StatusBar
          barStyle={isDark ? "light-content" : "dark-content"}
          backgroundColor="transparent"
        />
        {renderContent()}
      </View>
    </View>
  );
};

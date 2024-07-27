import { WebView } from 'react-native-webview';
import Constants from 'expo-constants';
import { StyleSheet } from 'react-native';


export default function App() {
  return (
    <WebView
      style={styles.container}
      originWhitelist={['*']}
      source={{ uri: 'https://c717-38-27-127-34.ngrok-free.app' }}
      // source={{ uri: 'http://172.16.21.83:8000' }}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Constants.statusBarHeight,
  },
});

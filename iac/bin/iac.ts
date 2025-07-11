import * as cdk from 'aws-cdk-lib';
import { IacStack } from '../lib/iac-stack';

const app = new cdk.App();
new IacStack(app, 'IacStack', {
  env: {
    account: '000000000000',    // ダミーのアカウントID
    region:  'ap-northeast-1',  // 東京リージョン
  },
  synthesizer: new cdk.BootstraplessSynthesizer(),
});
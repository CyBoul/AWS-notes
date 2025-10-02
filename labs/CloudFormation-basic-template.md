
https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-instance.html

```yaml
Resources:
  RobotAppServer:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: t2.micro
      ImageId: ami-087c17d1fe0178315
      SecurityGroups:
      - !Ref RobotAppSecurityGroup
  RobotAppSecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: Enable SSH access via port 22
      SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: '22'
        ToPort: '22'
        CidrIp: 0.0.0.0/0
  RobotS3Bucket:
    Type: 'AWS::S3::Bucket'
    DeletionPolicy: Delete
```

DIY: Create same template but with EC2 **t2.small** instance type
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
"""
导入数据
train_X:训练集特征集合   train_y:训练集标签集合
test_X:测试集特征集合    test_y：测试集标签集合
"""
train_X=np.loadtxt("./Iris/train/x.txt")
train_y=np.loadtxt("./Iris/train/y.txt")
test_X=np.loadtxt("./Iris/test/x.txt")
test_y=np.loadtxt("./Iris/test/y.txt")
print(train_X,'\n',train_y,'\n',test_X,'\n',test_y)#展示数据
"""创建Perceptron_3Classes_Mini_batch_Adam类
fit():训练数据的方法
Parameters:X,y
predict():预测数据分类情况
Parameter:X
Return:数据的类别
"""
class Perceptron_3Classes_Mini_batch_Adam():
    def __init__(self,alpha,times):#输入为学习率和迭代次数
        self.times=times
        self.alpha=alpha
    def fit(self,X,y):
        np.random.seed(2)#使特征集和标签集以相同顺序打乱
        self.X=np.random.permutation(np.insert(X,0,1,axis=1))#在特征集第一列插入1，并按行打乱其顺序
        np.random.seed(2)#使特征集和标签集以相同顺序打乱
        self.y=np.random.permutation(y.reshape(-1,1))#将标签集转化为列向量并打乱其顺序
        np.random.seed(2)#使每次运行的初始权值相同
        self.omiga=[np.random.randn(self.X.shape[1],3)]#按照标准高斯分别随机初始化权值
        self.cost=[]
        H_omiga = np.empty(self.y.shape)
        Num_batch=int(len(self.X)/16)#每个mini batch长度为16，计算mini batch的数量
        beta1 = 0.9#Adam算法参数
        beta2 = 0.999#Adam算法参数
        v0=v1 =v2= 0#Adam算法参数
        s0=s1 =s2= 0#Adam算法参数
        for i in range(self.times):
            for j in range(Num_batch):
                z=np.dot(self.X[j*16:j*16+16],self.omiga[i*Num_batch+j])
                H_omiga[j*16:j*16+16]=np.asarray(np.argmax(z,axis=1)).reshape(-1,1)#用上一次下降的权值计算每一个mini batch的预测值
                index0=np.arange(16).reshape(-1,1)#生成数组索引
                term1=z[(index0, H_omiga[j * 16:j * 16 + 16].astype(int))]#用预测标签计算乘积
                term2=z[(index0,self.y[j * 16:j * 16 + 16].astype(int))]#用属于第真实标签类的权值计算乘积
                J=np.sum(term1-term2)#在该mini batch内计算损失函数
                self.cost.append(J)
                g0=np.dot(self.X[j*16:j*16+16].T,np.where(H_omiga[j*16:j*16+16]==0,1,0)-np.where(self.y[j*16:j*16+16]==0,1,0))#omiga0的梯度
                v0 = beta1 * v0 + (1 - beta1) * g0
                v0_correct = v0 / (1 - beta1 ** (i * Num_batch + j + 1))
                s0 = beta2 * s0 + (1 - beta2) * (g0 ** 2)
                s0_correct = s0 / (1 - beta2 ** (i * Num_batch + j + 1))
                g0=v0_correct/(np.sqrt(s0_correct)+10**(-8))#用Adam算法优化梯度
                g1 =np.dot(self.X[j * 16:j * 16 + 16].T,np.where(H_omiga[j*16:j*16+16]==1,1,0) -np.where( self.y[j*16:j*16+16]==1,1,0 ))#omiga1的梯度
                v1 = beta1 * v1 + (1 - beta1) * g1
                v1_correct = v1 / (1 - beta1 ** (i * Num_batch + j + 1))
                s1 = beta2 * s1 + (1 - beta2) * (g1 ** 2)
                s1_correct = s1 / (1 - beta2 ** (i * Num_batch + j + 1))
                g1 = v1_correct / (np.sqrt(s1_correct) + 10 ** (-8))
                g2 = np.dot(self.X[j * 16:j * 16 + 16].T,np.where(H_omiga[j * 16:j * 16 + 16] ==2 , 1, 0) - np.where(self.y[j * 16:j * 16 + 16] == 2,1, 0))#omiga2的梯度
                v2 = beta1 * v2 + (1 - beta1) * g2
                v2_correct = v2 / (1 - beta1 ** (i * Num_batch + j + 1))
                s2 = beta2 * s2+ (1 - beta2) * (g2 ** 2)
                s2_correct = s2 / (1 - beta2 ** (i * Num_batch + j + 1))
                g2 = v2_correct / (np.sqrt(s2_correct) + 10 ** (-8))
                self.omiga.append(self.omiga[i*Num_batch+j]-self.alpha*np.hstack((g0,g1,g2))/16)#更新权值
    def predict(self,X):
        self.X=np.insert(X,0,1,axis=1)
        z = np.dot(self.X, self.omiga[-1])
        H_omiga = np.argmax(z, axis=1)
        return H_omiga
def Accuracy(X,y,omiga):#准确率计算函数
    X=np.insert(X,0,1,axis=1)
    z = np.dot(X, omiga)
    H_omiga = np.argmax(z, axis=1)
    return np.sum(np.where(H_omiga==y,1,0))/len(y)
aa=Perceptron_3Classes_Mini_batch_Adam(0.5,150)
aa.fit(train_X,train_y)#训练权值
train_y_hat=aa.predict(train_X)#预测训练集
test_y_hat=aa.predict(test_X)#预测测试集
print(aa.cost)#输出损失函数
ac_train=[]#训练集预测准确率
for i in range(600):
    ac_train.append(Accuracy(train_X,train_y,aa.omiga[i]))
ac_test=[]#测试集预测准确率
for i in range(600):
    ac_test.append(Accuracy(test_X,test_y,aa.omiga[i]))
print(ac_train,'\n',ac_test)#输出训练集和测试集预测准确率
"""
可视化
"""
fig,ax=plt.subplots(1,3,figsize=(15,5))#创建画布和坐标轴
ax[0].scatter(train_X[:,0],train_X[:,1],c=train_y,cmap='Dark2',s=10)#在第一个坐标轴上绘制训练集分布
ax[0].scatter(test_X[:,0],test_X[:,1],c=test_y,cmap='Dark2',s=10)#在第一个坐标轴上绘制测试集分布
ax[0].set_xlabel("Feature1")#设置x轴标签
ax[0].set_ylabel("Feature2")#设置y轴标签
ax[0].set_title("Classification Line")#设置标题
ax[1].set_xlim(0,599)#设置x轴范围
ax[1].set_ylim(0,150)#设置y轴范围
ax[1].set_xlabel("Iteration")#设置x轴标签
ax[1].set_ylabel("Cost Function")#设置y轴标签
ax[1].set_title("Cost Change")#设置标题
ax[2].set_xlim(0,599)
ax[2].set_ylim(0,1)
ax[2].set_xlabel("Iteration")#设置x轴标签
ax[2].set_ylabel("Accuracy")#设置y轴标签
ax[2].set_title("Accuracy Change")#设置标题
feature1 = np.linspace(1.5, 5, 400)#在1.5~5间均匀生成400个数,400比较大，会运行得久一些，但是生成的界限比较光滑
feature2 = np.linspace(0, 3, 400)#在0~3间均匀生成400个数
XX1, XX2 = np.meshgrid(feature1, feature2)#生成网格点坐标矩阵
XX=np.insert(np.c_[XX1.ravel(),XX2.ravel()], 0, 1, axis=1)#平铺并合并XX1和XX2，方便预测网格点上每个点的分类
z = np.dot(XX, aa.omiga[0])
yy = np.argmax(z, axis=1).reshape(np.shape(XX1))#预测网格点上每个点的分类
cont=ax[0].contourf(XX1,XX2,yy,alpha=0.2,cmap='Set3')#绘制决策界限
line1,=ax[1].plot([],[])#在第二个坐标轴上绘制损失函数下降情况
sca2=ax[2].scatter([],[],label='training set',s=10,c='red')#在第三个坐标轴上绘制训练集预测准确率变化情况
sca3=ax[2].scatter([],[],label='test set',s=10)#在第三个坐标轴上绘制测试集预测准确率变化情况
ite=np.arange(600)#迭代次数数组
def animate(i):#定义动画更新函数
    global cont
    for c in cont.collections:  # 加快动画运行速率
        c.remove()
    z = np.dot(XX, aa.omiga[i])
    yy = np.argmax(z, axis=1).reshape(np.shape(XX1))  # 根据权值更新预测情况
    cont = ax[0].contourf(XX1, XX2, yy, alpha=0.2, cmap='Set3')  # 更新决策界限
    line1.set_data(ite[:i],aa.cost[:i])
    sca2.set_offsets(np.stack((ite[:i],ac_train[:i]),axis=1))
    sca3.set_offsets(np.stack((ite[:i],ac_test[:i]),axis=1))
    return ax[0],line1,sca2,sca3
ani=animation.FuncAnimation(fig,animate,frames=600,interval=10)
plt.legend()
plt.show()
#ani.save('Perceptron_3Classes_Mini_batch_Adam.gif',writer='imagemagick',fps=60)#保存动态图（需要安装imagemagick）

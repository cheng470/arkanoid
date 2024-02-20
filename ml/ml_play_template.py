"""
The template of the main script of the machine learning process
"""

class MLPlay:
    def __init__(self,ai_name, *args, **kwargs):
        """
        Constructor
        """
        print(ai_name)
        self.ballPosOld = (0, 0)

    def update(self, scene_info, *args, **kwargs):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"
        if not scene_info["ball_served"]:
            return "SERVE_TO_LEFT"
        else:
            # 获取小球的位置(x1,y1) 移动速度为7
            # 还有平台的位置(x2,y2) 移动速度为5 平台尺寸是 40*5
            # 水平距离 |x1-x2| 垂直距离 |y1-y2| 屏幕尺寸是200*500
            # 怎样让平台一直能接到小球？
            # 如果球往上跑，则平台不需要移动
            # 如果球往下跑，则计算小球到达平台时的位置
            ballPos = scene_info["ball"]
            if self.ballPosOld[0] == 0 and self.ballPosOld[1] == 0:
                self.ballPosOld = ballPos
                return "NONE"
            if ballPos[1] < self.ballPosOld[1]:
                self.ballPosOld = ballPos
                return "NONE"

            platformPos = scene_info["platform"]
            t = (platformPos[1] - ballPos[1]) / 7 # 小球降落到平台所需要的时间

            isMoveLeft = ballPos[0] < self.ballPosOld[0]
            v = ballPos[0] - self.ballPosOld[0] # 小球 x 方向的速度
            if v < 0:
                v = -v

            x = ballPos[0] + v*t # 小球降落到平台时，小球的 x 坐标
            if isMoveLeft:
                x = ballPos[0] - v*t
            if x > 200:
                x = x % 400 # 不能大于400
                if x > 200:
                    x = 200 - (x - 200)
            if x < 0:
                x = -x
            #if isMoveLeft:
            #    x = (ballPos[0] - 7*t) % 200 # 小球降落到平台时，小球的 x 坐标
            
            # x 转为 5 的倍数
            x = x // 5 * 5
            print(f"ballPos={ballPos}, platformPos={platformPos}, isMoveLeft={isMoveLeft}, v={v}, t={t}, x={x}")
            if x == platformPos[0]+10:
                command = "NONE"
            elif x < platformPos[0]+10:
                command = "MOVE_LEFT"
            else:
                command = "MOVE_RIGHT"
            self.ballPosOld = ballPos

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

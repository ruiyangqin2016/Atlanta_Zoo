package package_login_register;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.Icon;
import javax.swing.JOptionPane;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JButton;
import javax.swing.JTextField;

public class LoginFrame extends JFrame implements ActionListener{
    private JLabel lbAccount=new JLabel("email/username");
    private JTextField tfAccount=new JTextField(10);
    private JLabel lbPassword=new JLabel("password           ");
    private JPasswordField pfPassword=new JPasswordField(10);
    private JButton btLogin=new JButton("login");
    private JButton btRegister=new JButton("register");
    private JButton btExit=new JButton("exit");
    public LoginFrame() {
        super("login");
        this.setLayout(new FlowLayout());
        this.add(lbAccount);
        this.add(tfAccount);
        this.add(lbPassword);
        this.add(pfPassword);
        this.add(btLogin);
        this.add(btRegister);
        this.add(btExit);
        this.setSize(240,180);
        GUIUtil.toCenter(this);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setResizable(false);
        this.setVisible(true);
        btLogin.addActionListener(this);
        btRegister.addActionListener(this);
        btExit.addActionListener(this);
    }
    @Override
    public void actionPerformed(ActionEvent e) {
        if(e.getSource()==btLogin) {
            String account=tfAccount.getText();
            String password=new String(pfPassword.getPassword());
            FileOpe.getInfoByAccount(account);
            if(Conf.account==null||!Conf.password.equals(password)) {
                JOptionPane.showMessageDialog(this,"登录失败");
                return;
            }
            JOptionPane.showMessageDialog(this,"登录成功");
            this.dispose();
            new OperationFrame();
        }
        else if(e.getSource()==btRegister) {
            this.dispose();
            new RegisterFrame();
        }
        else {
            JOptionPane.showMessageDialog(this,"谢谢光临");
            System.exit(0);
        }
    }
}
